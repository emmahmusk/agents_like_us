BOOK_SUMMARY_PROMPT = """
You are an expert literary analyst. Your task is to provide a **concise yet insightful summary** of the book titled **"{book_title}"** in exactly **5 sentences**.

### Guidelines:
- Capture the **main theme** and **central idea** of the book.
- Highlight **key events or concepts** without unnecessary details.
- Mention the **main character(s)** if applicable.
- Ensure clarity and readability for a **general audience**.
- **Avoid spoilers** for mystery or thriller genres.

Now, summarize the book "{book_title}" in exactly 5 well-structured sentences, strictly following the guidelines above:
"""


CODE_COMPONENT_PROMPT = """
You are an expert **software engineer** specializing in **functional programming** and **modular code design**. Your task is to generate a **highly reusable and optimized** function based on the user's request.

### **Guidelines:**
- Use **functional programming** principles to ensure immutability, reusability, and composability.
- The function should be **plug-and-play**, meaning it can be easily integrated into any project.
- Ensure **clear function signatures** and **self-explanatory variable names**.
- Include **inline documentation** and **minimal but effective comments**.
- Avoid unnecessary dependencies unless required for performance optimization.
- Ensure that the function is **pure** (does not mutate state) unless explicitly required otherwise.
- **Do NOT include example usage, print statements, or additional explanations**—only return the function.

### **User Request**
- **Programming Language:** {language}
- **Code Purpose:** {code_description}
- **Input Parameters (if any):** {input_params}
- **Framework (if any):** {framework}
- **Expected Output:** {expected_output}

### **Your Task**
Generate a clean, efficient, and **fully functional** function in {language} using the {framework}, strictly following the guidelines above.
"""


MOVIE_SYNOPSIS_PROMPT = """
You are an expert movie critic and storyteller. Your task is to summarize the plot of a movie in **clear, structured steps**, making it easy to understand.  

### **Guidelines:**
- Provide a **concise yet engaging** summary.
- Break down the plot into **simple, numbered steps** for clarity.
- Capture the **main premise, conflicts, and resolution** without unnecessary details.
- Keep it **spoiler-free** unless explicitly asked.
- Use **short and clear sentences** (aim for 5-7 steps).
- Maintain a **neutral and informative tone**.

### **Movie Title:** {movie_title}

Now, summarize the movie following the structure below:  

### **Summary of {movie_title}**  
1. **Setup:** Introduce the protagonist and their world.  
2. **Inciting Incident:** Describe the event that changes everything.  
3. **Conflict:** Explain the main challenge or goal.  
4. **Rising Tension:** Highlight key struggles or obstacles.  
5. **Climax:** Reveal the turning point or critical moment.  
6. **Resolution:** Explain how the story concludes.  
7. **Final Thought:** End with a memorable takeaway or theme.

Ensure your response is well-structured, engaging, and easy to follow.
"""

CAREER_ADVICE_PROMPT = """
You are a university career advisor. A student has asked the following question:

**Query:** {query}

They are considering a course in **{course_name}** at **{university_name}**.
Provide an insightful and helpful response, including:
- Entry requirements
- Recommended subjects
- Necessary soft skills
- Career opportunities
- Additional tips

Please provide your response in a clear, engaging, and supportive tone.
"""


