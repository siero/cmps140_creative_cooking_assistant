"""
Data structures used for communication between modules.
"""

class ConversationState(object):
    """
    Stores all state associated with a conversation.  Instances are
    created when a conversation begins and are passed throughout the
    application.  The receiver of a ConversationState will update the
    state by modifying the ConversationState that it receives.

    The ConversationState can be persisted by pickling it using the
    pickle or cPickle modules.

    This makes it easy to put the system into specific states for
    testing, without having to write complex test setup and teardown
    methods.
    """

    def __init__(self):
        self.user_name = ""
        self.last_user_input = ""
        self.current_state = "greeting"


class Message(object):
    """
    Base class for messages exchanged between the NLU and DM and DM
    and NLG.  It implements frame-and-slot semantics through its
    frame attribute, which is a dictionary.  It also stores metadata
    using its other attributes.
    """

    def __init__(self):
        """
        Create a new Message.
        """
        self.mood = None # Or some sensible default.
        # Frame implements frame-and-slot semantics.
        self.frame = {}
        # Additional metadata attributes could be added.


class ParsedInputMessage(Message):
    """
    Parsed representation of user input, generated by the NLU for use
    by the DM.
    """

    def __init__(self, raw_input_string):
        """
        Create a new ParsedInput.
        """
        Message.__init__(self)
        self.raw_input_string = raw_input_string

    def parse(self):
        """
        Fills out the message meta and frame attributes.
        """
        pass
        
    def confidence(self):
        """
        Returns a confidence value for the raw_input_string matching the
        message type.
        """
        return 0.0


class ContentPlanMessage(Message):
    """
    Representation of content to express to user, generated by the DM
    for use by the NLG.
    """

    def __init__(self, description):
        Message.__init__(self)
        self.description = description

    def __str__(self):
        return "<ContentPlanMessage: %s>" % self.description
