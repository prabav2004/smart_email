from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import settings


class EmailAgent:
    """
    Single reusable AI agent that handles generating professional responses
    tailored to various classified email categories using OpenAI.
    """
    def __init__(self):
        # Instantiate OpenAI chat model (uses settings api key)
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=settings.OPENAI_API_KEY,
            temperature=0.7
        )

        # Internal prompt definitions mapped by category
        self.prompts = {
            "Job": ChatPromptTemplate.from_messages([
                ("system", 
                 "You are a professional HR recruiter. Generate a polite and clear email response "
                 "acknowledging receipt of the user's job application/inquiry. Inform them that the "
                 "recruiting team is reviewing their profile and will reach out if there's a match. "
                 "Maintain a professional and welcoming tone."
                 ),
                ("human", "Email Content:\n{email}")
            ]),
            "Complaint": ChatPromptTemplate.from_messages([
                ("system", 
                 "You are a dedicated Customer Relations Specialist. Generate an empathetic, "
                 "professional response apologizing for the poor experience described in the email. "
                 "Assure the customer that their complaint has been escalated to senior management "
                 "and that you are working actively to resolve the issue as a top priority."
                 ),
                ("human", "Email Content:\n{email}")
            ]),
            "Sales": ChatPromptTemplate.from_messages([
                ("system", 
                 "You are an energetic Sales Representative. Generate a professional sales follow-up email. "
                 "Thank the sender for their interest, highlight that a sales manager will be reaching "
                 "out shortly, and offer to schedule a brief discovery call to explore details."
                 ),
                ("human", "Email Content:\n{email}")
            ]),
            "Personal": ChatPromptTemplate.from_messages([
                ("system", 
                 "You are a helpful personal assistant. Generate a warm, professional response acknowledging "
                 "receipt of the sender's email. Inform them that you will review it and follow up individually "
                 "at the earliest opportunity."
                 ),
                ("human", "Email Content:\n{email}")
            ])
        }

    def generate_reply(self, email: str, category: str) -> str:
        """
        Generates a professional reply for the email body using the prompt
        associated with the provided category.
        """
        # Fallback to Personal prompt if category doesn't match
        prompt = self.prompts.get(category, self.prompts["Personal"])
        
        # Format the prompt with inputs
        formatted_messages = prompt.format_messages(email=email)
        
        # Invoke LLM
        response = self.llm.invoke(formatted_messages)
        
        return str(response.content).strip()
