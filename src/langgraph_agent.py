from typing import TypedDict, Optional

import pandas as pd
from langgraph.graph import StateGraph, START, END

from .database import get_schema, execute_query
from .sql_generator import generate_sql
from .validator import validate_sql
from .agent import correct_sql


class AgentState(TypedDict, total=False):
    question: str
    schema: str
    sql: str
    data: Optional[pd.DataFrame]
    error: Optional[str]
    attempts: int
    success: bool
    history: list


MAX_RETRIES = 3


# =========================================================
# GENERATE SQL
# =========================================================

def generate_sql_node(state: AgentState):

    sql = generate_sql(
        state["question"],
        state["schema"]
    )

    history = state.get("history", [])

    history.append({
        "stage": "SQL Generation",
        "sql": sql
    })

    return {
        "sql": sql,
        "error": None,
        "history": history
    }


# =========================================================
# VALIDATE SQL
# =========================================================

def validate_sql_node(state: AgentState):

    valid, message = validate_sql(
        state["sql"]
    )

    history = state.get("history", [])

    if not valid:

        history.append({
            "stage": "SQL Validation",
            "status": "FAILED",
            "error": message,
            "sql": state["sql"]
        })

        return {
            "error": message,
            "success": False,
            "history": history
        }

    history.append({
        "stage": "SQL Validation",
        "status": "PASSED",
        "sql": state["sql"]
    })

    return {
        "error": None,
        "history": history
    }


# =========================================================
# EXECUTE SQL
# =========================================================

def execute_sql_node(state: AgentState):

    current_attempt = state.get("attempts", 0) + 1

    df, error = execute_query(
        state["sql"]
    )

    history = state.get("history", [])

    # -------------------------
    # Execution failed
    # -------------------------

    if error is not None:

        history.append({
            "stage": "SQL Execution",
            "attempt": current_attempt,
            "status": "FAILED",
            "error": error,
            "sql": state["sql"]
        })

        return {
            "data": None,
            "error": error,
            "success": False,
            "attempts": current_attempt,
            "history": history
        }

    # -------------------------
    # Execution successful
    # -------------------------

    history.append({
        "stage": "SQL Execution",
        "attempt": current_attempt,
        "status": "PASSED",
        "rows": len(df),
        "sql": state["sql"]
    })

    return {
        "data": df,
        "error": None,
        "success": True,
        "attempts": current_attempt,
        "history": history
    }


# =========================================================
# SELF CORRECTION
# =========================================================

def correction_node(state: AgentState):

    corrected_sql = correct_sql(
        question=state["question"],
        sql=state["sql"],
        error=state["error"],
        schema=state["schema"]
    )

    history = state.get("history", [])

    history.append({
        "stage": "Self-Correction",
        "status": "COMPLETED",
        "previous_error": state["error"],
        "corrected_sql": corrected_sql
    })

    return {
        "sql": corrected_sql,
        "error": None,
        "history": history
    }


# =========================================================
# ROUTING AFTER VALIDATION
# =========================================================

def validation_route(state: AgentState):

    if state.get("error") is None:
        return "execute"

    return "correct"


# =========================================================
# ROUTING AFTER EXECUTION
# =========================================================

def retry_or_finish(state: AgentState):

    if state.get("success"):
        return "success"

    if state.get("attempts", 0) >= MAX_RETRIES:
        return "failed"

    return "retry"


# =========================================================
# INITIAL ROUTE
# =========================================================

def initial_route(state: AgentState):

    # If SQL was already supplied,
    # use it directly for testing/self-correction.

    if state.get("sql", "").strip():

        return "validate"

    # Otherwise generate SQL normally.

    return "generate"


# =========================================================
# BUILD LANGGRAPH
# =========================================================

def build_graph():

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node(
        "generate_sql",
        generate_sql_node
    )

    graph.add_node(
        "validate_sql",
        validate_sql_node
    )

    graph.add_node(
        "execute_sql",
        execute_sql_node
    )

    graph.add_node(
        "correct_sql",
        correction_node
    )

    # -----------------------------------------------------
    # START
    # -----------------------------------------------------

    graph.add_conditional_edges(
        START,
        initial_route,
        {
            "generate": "generate_sql",
            "validate": "validate_sql"
        }
    )

    # -----------------------------------------------------
    # Generate → Validate
    # -----------------------------------------------------

    graph.add_edge(
        "generate_sql",
        "validate_sql"
    )

    # -----------------------------------------------------
    # Validate → Execute / Correct
    # -----------------------------------------------------

    graph.add_conditional_edges(
        "validate_sql",
        validation_route,
        {
            "execute": "execute_sql",
            "correct": "correct_sql"
        }
    )

    # -----------------------------------------------------
    # Execute → Success / Retry / Failed
    # -----------------------------------------------------

    graph.add_conditional_edges(
        "execute_sql",
        retry_or_finish,
        {
            "success": END,
            "retry": "correct_sql",
            "failed": END
        }
    )

    # -----------------------------------------------------
    # Correction → Validate again
    # -----------------------------------------------------

    graph.add_edge(
        "correct_sql",
        "validate_sql"
    )

    return graph.compile()


# =========================================================
# PUBLIC AGENT FUNCTION
# =========================================================

def run_langgraph_agent(question: str):

    schema = get_schema()

    initial_state: AgentState = {
        "question": question,
        "schema": schema,
        "sql": "",
        "data": None,
        "error": None,
        "attempts": 0,
        "success": False,
        "history": []
    }

    app = build_graph()

    return app.invoke(initial_state)