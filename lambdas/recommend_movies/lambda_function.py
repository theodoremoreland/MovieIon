# First party
import json

# Custom
from modules.create_recommendation_samples import create_recommendation_samples
from modules.model import best_recommendations, worst_recommendations


def lambda_handler(event, context):
    # TODO implement
    return {
        "statusCode": 200,
        "body": json.dumps("Hello from Lambda!"),
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
    }
