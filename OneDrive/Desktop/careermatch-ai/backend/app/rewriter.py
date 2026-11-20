# rewriter.py

import os
import json

from .schemas import BulletSuggestion


async def improve_bullets(
    resume_text: str,
    job_text: str,
    fallback: list[BulletSuggestion]
):

    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        return fallback

    try:

        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=api_key)

        response = await client.chat.completions.create(

            model=os.getenv(
                "OPENAI_MODEL",
                "gpt-4o-mini"
            ),

            temperature=0.2,

            response_format={
                "type": "json_object"
            },

            messages=[

                {
                    "role": "system",

                    "content": (
                        "You are a careful professional resume editor. "
                        "Return JSON containing a suggestions array. "
                        "Each item must have original_context, "
                        "suggested_bullet and reason. "
                        "Only use facts explicitly present in the resume. "
                        "Never invent metrics, qualifications, tools, "
                        "responsibilities or achievements. "
                        "Use placeholders for missing verified results."
                    )
                },

                {
                    "role": "user",

                    "content": (
                        f"RESUME:\n{resume_text[:12000]}\n\n"
                        f"JOB DESCRIPTION:\n{job_text[:8000]}\n\n"
                        "Rewrite up to 3 relevant experience bullets."
                    )
                }

            ]

        )

        data = json.loads(
            response.choices[0].message.content or "{}"
        )

        suggestions = [

            BulletSuggestion(**item)

            for item in data.get("suggestions", [])[:3]

        ]

        return suggestions or fallback

    except Exception:

        return fallback
