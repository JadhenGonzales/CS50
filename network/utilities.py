import json
from typing import Tuple, Optional

from network.models import Profile, Post


def check_json(raw_data) -> Tuple[Optional[dict], Optional[str]]:
    """
    Accepts JSON and checks if the required fields are present. 
    Outputs the cleaned data or an error message.
    Expected data has {id, action, modifier/content}
    """

    required_fields = {'id', 'action'}
    actions = {'like', 'follow', 'edit'}

    # Check if data is complete
    data = json.loads(raw_data)

    if not all(field in data for field in required_fields):
        return None, 'Incomplete JSON data'
    
    # Get to avoid key errors
    id = data.get('id')
    action = data.get('action')
    modifier = data.get('modifier')
    text = data.get('text')
    
    # Check if data contents are valid
    if not isinstance(id, int):
        return None, 'ID must be an integer'
    if not isinstance(action, str):
        return None, 'Action must be a str'
    
    # Fill clean_data dictionary
    if action == 'follow':
        model = Profile
        if not isinstance(modifier, bool):
            return None, 'Following must have a boolean modifier'
        clean_data = {'modifier': modifier}
    
    elif action == 'like':
        model = Post
        if not isinstance(modifier, bool):
            return None, 'Liking must have a boolean modifier'
        clean_data = {'modifier': modifier}

    elif action == 'edit':
        model = Post
        if not isinstance(text, str):
            return None, 'Editing must contain the new post text'
        if not text:
            return None, 'Edit must not be empty'
        clean_data = {'text': text}

    else:
        return None, 'Invalid action'


    # Check ID validity
    try:
        target = model.objects.get(pk=id)
    except model.DoesNotExist:
        return None, f'ID: {id} not found'
    
    return {**clean_data, 'target':target}, None