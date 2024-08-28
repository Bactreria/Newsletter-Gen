#!/usr/bin/env python
import sys
from newsletter_crew.crew import NewsletterCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
def load_html_template():
    with open('C:/Users/Pavan/Desktop/newsletter_crew/src/newsletter_crew/config/newsletter_template.html', 'r') as file:
        html_template = file.read()
    return html_template




def run():
    """
    Run the crew.
    """
    inputs = {
        "topic": input("Enter the topic: "),
        "personal_message":"",
        "html_template": load_html_template(),
    }
    NewsletterCrew().crew().kickoff(inputs=inputs)


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         NewsletterCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         NewsletterCrew().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")
