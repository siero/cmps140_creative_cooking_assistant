import os
import random
from simplenlg import NPPhraseSpec, PPPhraseSpec, SPhraseSpec, Realiser, gateway, InterrogativeType, TextSpec, Tense, Form

class NLG(object):

    def __init__(self):
        """
        Creates a new Natural Lanaguage Generator.
        
        conf_responses: a list of preconfigured templates to express 
                        acknowledgement of input or action
        aff_responses: a list of preconfigured templates to express 
                       affirmation or to say 'yes'
        neg_responses: a list of preconfigured templates to express
                       decline of request or action or to say 'no'
        """

        self.conf_responses = ['You got it',
                              'As you wish',
                              'You don\'t have to ask me twice',
                              'Of course',
                              'Okay',
                              'Acknowledged']
 
        self.aff_responses = ['Yes',
                              'Yeah',
                              'Very much so',
                              'Affirmative']

        self.neg_responses = ['No',
                              'Nah',
                              'Negative',
                              'I\'m afraid not']

        self.search_verbs = ['look for',
                             'search for',
                             'bring you',
                             'seek',
                             'find']

        self.words = {'name':'Jeraziah',
                      'subject':'you', 
                      'verb':'prefer', 
                      'object':'recipes',
                      'preposition':'that contains',
                      'objmodifiers':['Thai'],
                      'prepmodifiers':['potatoes','celery','carrots'],
                      'adverbs':['confidently'],
                      'lastinput':'Sing me a song.'}

        self.query = {'include_ingredients':['chicken', 'pineapple', 'pepper'],
                      'exclude_ingredients':['dishwashing soap', 'salt'],
                      'include_cuisines':['Mexican', 'Chinese', 'Thai']}

        self.realiser = Realiser()

        print 'nlg creation successful'

    def generate_recipe(self, recipe):
        """
        Receives a Recipe object and displays its contents to the user.
        """

        output = []

        cuisines_str = 'Cuisines: ' + ', '.join(c.name for c in recipe.cuisines)

        output.append('Here is the recipe you requested: \n')
        output.append(HORIZONTAL_LINE)
        output.append(recipe.title + ' by ' + recipe.author)
        output.append(cuisines_str + '\n')
        output.append(recipe.description + '\n')
        output.append(recipe.ingredients_text + '\n')
        output.append(recipe.servings)
        if recipe.prep_time:
            output.append('Prep time: %i minutes' % (recipe.prep_time))
        if recipe.cook_time:
            output.append('Cook time: %i minutes' % (recipe.cook_time))
        if recipe.total_time:
            output.append('Total time: %i minutes\n' % (recipe.total_time))
        output.append(recipe.ingredients_text + '\n')
        output.append(recipe.steps_text)
        output.append(HORIZONTAL_LINE)

        return '\n'.join(output)

    def generate(self, utter_type, keywords, query=None):
        """
        Input: a type of inquiry to create and a dictionary of keywords.
        Types of inquiries include 'what', 'who', 'where', 'why', 'how', 
        and 'yes/no' questions. Alternatively, 'none' can be specified to
        generate a declarative statement.
        The dictionary is essentially divided into three core parts: the
        subject, the verb, and the object. Modifiers can be specified to these
        parts (adverbs, adjectives, etc). Additionally, an optional
        prepositional phrase can be specified.

        Example: 

        >>> nlg = NLG()
        nlg creation successful
        >>> words = {'subject':'you', 
        ...         'verb':'prefer', 
        ...         'object':'recipes',
        ...         'preposition':'that contains',
        ...         'objmodifiers':['Thai'],
        ...         'prepmodifiers':['potatoes','celery','carrots'],
        ...         'adverbs':['confidently']}
        >>> print nlg.generate('yes_no', nlg.words)
        Do you confidently prefer Thai recipes that contains potatoes, celery and carrots?
        >>> print nlg.generate('how', words)
        How do you confidently prefer Thai recipes that contains potatoes, celery and carrots?
        """

        if utter_type.lower() == 'greet':
            if 'name' in keywords:
                return'Hello, %s!' % (keywords['name'])
            else:
                return 'Hello there!'
            return

        if utter_type.lower() == 'echo':
            if 'lastinput' in keywords:
                return keywords['lastinput']

        utterance = SPhraseSpec()
        subject = NPPhraseSpec(keywords['subject'])
        target = NPPhraseSpec(keywords['object'])
        preposition = PPPhraseSpec()
        
        if 'preposition' in keywords:
            preposition.setPreposition(keywords['preposition'])

        if 'prepmodifiers' in keywords:
            for modifier in keywords['prepmodifiers']:
                preposition.addComplement(modifier)

        if 'submodifiers' in keywords:
            for modifier in keywords['submodifiers']:
                subject.addModifier(modifier)

        if 'objmodifiers' in keywords:
            for modifier in keywords['objmodifiers']:
                target.addModifier(modifier)

        if utter_type.lower() == 'yes_no':
            utterance.setInterrogative(InterrogativeType.YES_NO)
        elif utter_type.lower() == 'how':
            utterance.setInterrogative(InterrogativeType.HOW)
        elif utter_type.lower() == 'what':
            utterance.setInterrogative(InterrogativeType.WHAT)
        elif utter_type.lower() == 'where':
            utterance.setInterrogative(InterrogativeType.WHERE)
        elif utter_type.lower() == 'who':
            utterance.setInterrogative(InterrogativeType.WHO)
        elif utter_type.lower() == 'why':
            utterance.setInterrogative(InterrogativeType.WHY)
        elif utter_type.lower() == 'confirm':
            return self.acknowledge(keywords)
        elif utter_type.lower() == 'affirm':
            return self.affirm(keywords)
        elif utter_type.lower() == 'decline':
            return self.decline(keywords)
        elif utter_type.lower() == 'unknown':
            return self.unknown(keywords)
        elif utter_type.lower() == 'summarize':
            return random.choice([self.acknowledge(keywords) + '\n', '']) + self.summarize_query(query)

        target.addModifier(preposition)
        utterance.setSubject(keywords['subject'])
        utterance.setVerb(keywords['verb'])
        if 'adverbs' in keywords:
            for modifier in keywords['adverbs']:
                utterance.addModifier(modifier)
        utterance.addComplement(target)
        
        output = self.realiser.realiseDocument(utterance).strip()
        return output

    def acknowledge(self, keywords):
        """
        Returns an utterance of acknowledgement at random.
        A template is picked randomly from preconfigured choices.
        Then, the choice of adding the user's name is randomly determined.
        Finally, either a period or exclamation mark is used to end the
        sentence.
        """

        acknowledgement = random.choice(self.conf_responses)
        if 'name' in keywords:
            acknowledgement += random.choice([', ' + keywords['name'], ''])
        return acknowledgement + random.choice(['.', '!'])

    def affirm(self, keywords):
        """
        Returns an utterance of affirmation at random.
        A template is picked randomly from preconfigured choices.
        Then, the choice of adding the user's name is randomly determined.
        Finally, either a period or exclamation mark is used to end the
        sentence.
        """

        affirmation = random.choice(self.aff_responses)
        if 'name' in keywords:
            affirmation += random.choice([', ' + keywords['name'], ''])
        return affirmation + random.choice(['.', '!'])

    def decline(self, keywords):
        """
        Returns an utterance of denial or decline of action.
        A template is picked randomly from preconfigured choices.
        Then, the choice of adding the user's name is randomly determined.
        Finally, either a period or exclamation mark is used to end the
        sentence.
        """

        decline = random.choice(self.neg_responses)
        if 'name' in keywords:
            decline += random.choice([', ' + keywords['name'], ''])
        return decline + random.choice(['.', '!'])

    def unknown(self, keywords):
        """
        Returns an utterance that tells the user the last input was not
        understood.
        """

        output = SPhraseSpec()
        output.setSubject('I')
        output.setComplement('you')
        output.setTense(Tense.PAST)

        choice = random.randint(1, 3)
        if choice == 1:
            output.setVerb('understand')
            output.setComplement('what you')
            output.setNegated(gateway.jvm.java.lang.Boolean.TRUE)
            output.setPostmodifier('just said')
        elif choice == 2:
            output.setInterrogative(InterrogativeType.WHAT)
            output.setVerb('do')
            output.setPostmodifier('say')
        elif choice == 3:
            output.setTense(Tense.PRESENT)
            output.setSubject('please rephrase')
            output.setComplement('what you')
            output.setPostmodifier('just said')

        return self.realiser.realiseDocument(output).strip()

    def summarize_query(self, query):
        """
        Returns an utterance that rewords the inputted query as a form
        of acknowledgement to the user.
        """

        # if no criteria is provided, let the user know that every dish
        # will be searched
        if query == {}:
            return 'I will just look for every recipe we have.'

        summary = SPhraseSpec()
        summary.setSubject('I')
        summary.setVerb(random.choice(self.search_verbs))
        summary.setProgressive(gateway.jvm.java.lang.Boolean.TRUE)

        # add specified cuisines included, if they exist
        if 'include_cuisines' in query:
            for cuisine in query['include_cuisines']:
                if cuisine == query['include_cuisines'][-1]:
                    summary.addComplement(cuisine + ' dishes')
                else:
                    summary.addComplement(cuisine)
        else:
            summary.addComplement('recipes')

        # create phrase to include ingredients
        if 'include_ingredients' in query:
            ing_inc = PPPhraseSpec()
            ing_inc.setPreposition('that contain')
            for ingredient in query['include_ingredients']:
                ing_inc.addComplement(ingredient)
            summary.addModifier(ing_inc)

        # create phrase to exclude ingredients
        if 'exclude_ingredients' in query:
            ing_exc = PPPhraseSpec()
            ing_exc.setPreposition('but do not contain')
            for ingredient in query['exclude_ingredients']:
                ing_exc.addComplement(ingredient)
            summary.addModifier(ing_exc)

        # create phrase to include recipe times and number of steps
        # and/or ingredients

        steps = SPhraseSpec()
        if 'prep_time' in query or 'cook_time' in query or 'total_time' in query or 'num_steps' in query or 'num_ingredients' in query:
            steps.setSubject('I')
            steps.setVerb(random.choice(self.search_verbs))
            steps.setProgressive(gateway.jvm.java.lang.Boolean.TRUE)
            steps.addPremodifier('also')

            steps_list = []
            if 'prep_time' in query and query['prep_time'] != None:
                steps_list.append('%i minutes to prepare' % query['prep_time'])
            if 'cook_time' in query and query['cook_time'] != None:
                steps_list.append('%i minutes to cook' % (query['cook_time']))
            if 'total_time' in query and query['total_time'] != None:
                steps_list.append('%i total minutes to make' % 
                                  (query['total_time']))
            if 'num_steps' in query and query['num_steps'] != None:
                steps_list.append('%i steps to complete' % (query['num_steps']))
            if 'num_ingredients' in query and query['num_ingredients'] != None:
                steps_list.append('%i ingredients' % (query['num_ingredients']))
            for step in steps_list:
                if step == steps_list[0]:
                    steps.addComplement('recipes that require ' + step)
                else:
                    steps.addComplement(step)

        # tie everything together into one utterance
        final = TextSpec()
        final.addSpec(summary)
        final.addSpec(steps)
        final.setListConjunct('.')

        return self.realiser.realiseDocument(final).strip()

class NLGException(Exception):
    """
    Base class for throwing exceptions related to the NLG
    """

    pass
