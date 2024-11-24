"""Code for the Custom Collage AI Agent."""
import os
from dotenv import load_dotenv
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI

load_dotenv()

# Initialize the language model (assuming you have an OpenAI key and library setup)
curr_model = 'gpt-4o-mini'
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables")

collage_ai = OpenAI(model=curr_model) 

# # TODO: Placeholder for the database of student backgrounds
# # In a real implementation, this would be connected to an actual database
# student_database: Dict[str, Any] = {
#     "Jaden": {
#         "keywords": "CS Math major UMich Machine Learning Intern Capital One cybersecurity",
#         "career_goal": "Software Engineer"
#     },
#     "Alex": {
#         "keywords": "Business major marketing entrepreneurship UMich Ross",
#         "career_goal": "COO"
#     }
# }

# # TODO: Placeholder for the database of courses
# courses_database: List[Dict] = {
#     {
#         "CourseName": "EECS 281",
#         "CombinedDescription": "Introduction to algorithm analysis and O-notation Fundamental data structures including lists, stacks, queues, priority queues, hash tables, binary trees, search trees, balanced trees and graphs; searching and sorting algorithms; recursive algorithms; basic graph algorithms; introduction to greedy algorithms and divide and conquer strategy. Several programming assignments"
#     },
#     {
#         "CourseName": "EECS 445",
#         "CombinedDescription": "Theory and implementation of state-of-the-art machine learning algorithms for large-scale real-world applications. Topics include supervised learning (regression, classification, kernel methods, neural networks, and regularization) and unsupervised learning (clustering, density estimation, and dimensionality reduction). For each topic, mathematical principles, key algorithmic ideas, and implementation will be highlighted."
#     },
#     {
#         "CourseName": "EECS 485",
#         "CombinedDescription": "Concepts surrounding web systems, applications, and internet scale distributed systems. Topics covered include client/server protocols, security, information retrieval and search engines, scalable data processing, and fault tolerant systems. The course has substantial projects involving development of web applications and web systems."
#     },
#     {
#         "CourseName": "TO 618",
#         "CombinedDescription": "Objective: Strategic and tactical decisions problems that firms face became too complex to solve by naive intuition and heuristics. Increasingly, making business decisions requires \"intelligent\" and \"data oriented\" decisions, aided by decision support tools and analytics. The ability to make such decisions and use available tools is critical for both managers and firms. In recent years, the toolbox of business analytics has grown. These tools provide the ability to make decisions supported by data and models. This course prepares students to model and manage business decisions with data analytics and decision models. Specifically, the course aims to achieve the following goals: A. To develop the ability to identify key drivers in business decisions and develop analytical models for prediction and prescription. B. To learn a variety of tools and techniques for a range of tactical, operational, and strategic business decision problems that apply in a broad range of problems. C. To develop the ability to communicate the results and findings of analytical solutions to different. Specifically, the course will cover descriptive analytics (e.g., data visualization, query, data slicing), predictive analytics (e.g., forecasting, classification, simulation), and prescriptive analytics (e.g., optimization). Examples include decision problems in supply chain and logistics, retail revenue management, finance, and risk management."
#     }
# }


# # Function to retrieve student information from the database
# def get_student_info(student_id: str) -> Dict[str, Any]:
#     return student_database.get(student_id, {"error": "Student not found."})


# Function to generate a response using OpenAI's language model
def generate_response(prompt, question) -> str:
    agent = OpenAIAgent.from_tools(
        llm=collage_ai,
        verbose=True,
        system_prompt=prompt,
    )
    response = agent.chat(question)
    return str(response)


def form_prompt(name, keywords, career_goal):
    return (
        f"You are a Collage AI assistant with the following student information:\n"
        f"Please introduce yourself as the Collage AI Assistant (Collage, not College) at the first response"
        f"Student Name: {name}"
        f"Keywords in the student's profile: {keywords}\n"
        f"Career Goal of the student: {career_goal}\n\n"
        f"Provide a detailed and informative response."
    )

def form_prompt_2(course_name, course_description, credits, department, tags, active_tab):
    print(course_name)
    return (
        f"You are the Collage AI Assistant. Please introduce yourself as the Collage AI Assistant "
        f"(Collage, not College) at the first response.\n\n"
        f"Course Details (Don't include these in your final response):\n"
        f"Name: {course_name}\n"
        f"Description: {course_description}\n"
        f"Credits: {credits}\n"
        f"Department: {department}\n"
        f"Tags: {tags}\n\n"
        f"Category: {active_tab}\n\n"
        f"Please provide a short response (less than 50 words) for the user's question "
        f"based on the course details and the selected category."
    )

# Chatbot function to handle user input and respond appropriately
def collage_ai_agent(user_input: str, prompt: str) -> str:
    # Generate a response based on the AI model, user input, and constructed prompt
    response = generate_response(user_input, prompt)
    return response


# TODO: Example usage of the chatbot in a simple interactive loop
# This is just for stand-alone testing of the Agent
def main():
    print("Welcome to the Collage AI Assistant!")
    print("Format: <student_id>: <your question>")
    print("Example: Jaden: What classes do you recommend?")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = collage_ai_agent(user_input)
        print(f"Collage AI Assistant: {response}")


if __name__ == "__main__":
    main()
