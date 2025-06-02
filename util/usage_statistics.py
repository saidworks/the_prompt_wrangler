def extract_metadata(ai_message, start_time=None, end_time=None):
    """
    Extract total token usage and response time from an AIMessage object.

    Args:
        ai_message (AIMessage): The LangChain AIMessage response object.
        start_time (float, optional): Time before the LLM call.
        end_time (float, optional): Time after the LLM call.

    Returns:
        dict: Contains 'total_tokens' and optionally 'response_time'.
    """
    metadata = {}

    try:
        metadata['total_tokens'] = ai_message.response_metadata['token_usage']['total_tokens']
    except (AttributeError, KeyError, TypeError):
        metadata['total_tokens'] = None

    if start_time is not None and end_time is not None:
        metadata['response_time'] = round(end_time - start_time, 3)
    else:
        metadata['response_time'] = None

    return metadata
