import openai
import re
openai.api_key = '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'


# Handle cases that produce outputs which are not strictly integers:
def convert_string(content):
    try:
        result = int(content)
    except ValueError:
        match = re.search(r'\d+', content)
        if match:
            result = int(match.group())
        else:
            result = 5

    return result


def score(question, answer):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"Score the given answer to the following question out of 10, 4 points for Accuracy, 3 points for Comprehensiveness, and 3 points for Clarity and Communication. Be strict but fair about the scoring, if an answre is incomplete, irrelevant or nonsensical, score it low. Give 0 points for answers like 'I don't know' and score very low for short incomplete answers (e.g. 'Yes', 'No, it won't', etc) answers that offer no explanation. There is no need to give grace marks, be strict in scoring. Return as output just a single number as the score, and nothing else at all. Input: Question: {question} Answer: {answer}"}]
    )

    score = convert_string(response.choices[0].message.content.strip())

    return score