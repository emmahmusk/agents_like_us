import os

from django.http import JsonResponse
import requests
from .sanitzer import sanitize_code_output
import google.generativeai as genai # type: ignore
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .prompts import BOOK_SUMMARY_PROMPT, CODE_COMPONENT_PROMPT, MOVIE_SYNOPSIS_PROMPT
from rest_framework.parsers import MultiPartParser


# Define a directory to save generated code files
CODE_OUTPUT_DIR = os.path.join(os.getcwd(), "generated_code")  # Change as needed

# Ensure the directory exists
os.makedirs(CODE_OUTPUT_DIR, exist_ok=True)

# Configure Google Gemini API
genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)

class BookSummaryView(APIView):
    def post(self, request):
        book_title = request.data.get("book_title")

        if not book_title:
            return Response({"error": "Book title is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")  # Use Gemini-Pro model
            user_query = BOOK_SUMMARY_PROMPT.format(book_title=book_title)
            response = model.generate_content(user_query)

            # Extract response text
            summary = response.text if response else "No response generated."

            return Response({"book_title": book_title, "summary": summary}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CodeComponentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data  
            language = data.get("language", "Python").strip()
            code_description = data.get("code_description")
            input_params = data.get("input_params", "N/A")
            framework = data.get("framework", "N/A")
            expected_output = data.get("expected_output", "N/A")

            if not code_description:
                return Response({"error": "Code description is required"}, status=status.HTTP_400_BAD_REQUEST)

            prompt = CODE_COMPONENT_PROMPT.format(
                language=language,
                code_description=code_description,
                input_params=input_params,
                framework=framework,
                expected_output=expected_output
            )

            # Generate code using Gemini
            model = genai.GenerativeModel("gemini-1.5-flash")  
            response = model.generate_content(prompt)

            code_snippet = response.text.strip() if response and response.text else "No code generated."
            # Sanitize the output
            code_snippet = sanitize_code_output(language, code_snippet)

            # Determine correct file extension
            file_extensions = {"python": "py", "javascript": "js", "dart": "dart", "php": "php"}
            file_extension = file_extensions.get(language.lower(), "txt")  

            filename = f"{language.lower()}_generated_code.{file_extension}"
            file_path = os.path.join(CODE_OUTPUT_DIR, filename)

            os.makedirs(CODE_OUTPUT_DIR, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(code_snippet)

            return Response({
                "language": language,
                "code_description": code_description,
                "generated_code": code_snippet,
                "file_path": file_path
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MovieSynopsisView(APIView):
    def post(self, request):
        movie_title = request.data.get("movie_title")

        if not movie_title:
            return Response({"error": "Movie title is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")  # Use Gemini AI Model
            user_query = MOVIE_SYNOPSIS_PROMPT.format(movie_title=movie_title)
            response = model.generate_content(user_query)

            # Extract response text and ensure a valid response
            synopsis = response.text.strip() if response and response.text else "No summary available."

            return Response({"movie_title": movie_title, "synopsis": synopsis}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MovieSearchView(APIView):
    def post(self, request):
        search_query = request.data.get("query", "latest movies")  # Default to latest movies

        if not search_query:
            return JsonResponse({"error": "Search query is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Step 1: Fetch Data from Google Search
            google_api_key = settings.GOOGLE_API_KEY
            search_engine_id = settings.GOOGLE_CSE_ID
            google_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&key={google_api_key}&cx={search_engine_id}"
            response = requests.get(google_url)
            search_results = response.json()

            # Step 2: Extract Movie Titles
            movie_titles = [item["title"] for item in search_results.get("items", [])[:5]]  # Limit to 5 results

            if not movie_titles:
                return JsonResponse({"error": "No results found"}, status=status.HTTP_404_NOT_FOUND)

            # Step 3: Use Gemini to Generate Insights
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"Here are some recent movie names: {', '.join(movie_titles)}. Can you summarize their genres and general themes?"
            gemini_response = model.generate_content(prompt)

            return JsonResponse({
                "query": search_query,
                "movies": movie_titles,
                "gemini_insights": gemini_response.text if gemini_response else "No insights generated."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)