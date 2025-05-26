import pandas as pd
import os
import re
import json
from dotenv import load_dotenv
from app.interfaces import CallbackHandler
from app.common import AppContext
import requests
from app.common.utilities import delete_file
from typing import Dict
from app.dtos.trainee_evaluation import TraineeEvaluation
from datetime import datetime
from datetime import timezone
load_dotenv('.env', override=True)

class EvaluateTrainees(CallbackHandler):
    def __init__(self, context: AppContext):
        self.ctx = context
        self.excel_reader = self.ctx.excel_reader

    async def download_csv_from_payload(self, payload: Dict) -> str:
        """
        Downloads the attached CSV file from the Lark payload and saves it to ./storage/et/.
        Skips download if file already exists.
        """
        try:
            self.ctx.logger.info("📥 Downloading Excel File")
            file_info = payload["file"][0]
            print(payload)
            file_name = f"data-{payload['uploaded_by'][0]['id']}.csv"
            file_path = os.path.join("storage", "et", file_name)

            if os.path.exists(file_path):
                self.ctx.logger.info(f"📂 File already exists. Skipping download: {file_path}")
                return file_path

            file_token = file_info["file_token"]
            record_id = payload["record_id"]

            # Prepare payload
            download_payload = {
                "file_token": file_token,
                "record_id": record_id
            }

            # Perform download
            await self.ctx.base_manager.adownload(
                payload=download_payload,
                folder_name="storage/et",
                file_name=file_name
            )

            self.ctx.logger.info(f"✅ File downloaded successfully: {file_path}")
            return file_path

        except Exception as e:
            self.ctx.logger.error(f"❌ Failed to download file from payload: {e}")
            raise

    def parse_evaluation_result(self, result: str) -> Dict:
        """
        Parse the evaluation result string into structured data.
        """
        # Ensure the input is treated as a string, handle potential None or non-string types
        if not isinstance(result, str) or not result or result.strip().upper() == "N/A":
            return {
                "final_score": None,
                "engagement": None,
                "knowledge": None,
                "critical_thinking": None,
                "minigame_score": None
            }

        # Clean up potential leading/trailing whitespace
        result = result.strip()

        try:
            # Extract final score (case-insensitive and flexible)
            final_score_match = re.search(r'final score: (\d+)/100', result, re.IGNORECASE)
            final_score = int(final_score_match.group(1)) if final_score_match else None

            # Extract engagement score
            engagement_match = re.search(r'engagement \((\d+)/30\)', result, re.IGNORECASE)
            engagement = int(engagement_match.group(1)) if engagement_match else None

            # Extract knowledge score
            knowledge_match = re.search(r'knowledge \((\d+)/40\)', result, re.IGNORECASE)
            knowledge = int(knowledge_match.group(1)) if knowledge_match else None

            # Extract critical thinking score
            critical_thinking_match = re.search(r'critical thinking \((\d+)/30\)', result, re.IGNORECASE)
            critical_thinking = int(critical_thinking_match.group(1)) if critical_thinking_match else None

            # Extract minigame score
            minigame_match = re.search(r'minigame score: (\d+)(?:/10)?', result, re.IGNORECASE)
            minigame_score = int(minigame_match.group(1)) if minigame_match and minigame_match.group(1).isdigit() else None

            return {
                "final_score": final_score,
                "engagement": engagement,
                "knowledge": knowledge,
                "critical_thinking": critical_thinking,
                "minigame_score": minigame_score
            }
        except Exception as e:
            self.ctx.logger.error(f"Error parsing evaluation result '{result}': {e}")
            return {
                "final_score": None,
                "engagement": None,
                "knowledge": None,
                "critical_thinking": None,
                "minigame_score": None
            }

    async def handler(self, payload: Dict[str, str]):
        self.ctx.logger.info("📝 Starting trainee evaluation...")
        try:
            # Download the CSV file
            file_path = await self.download_csv_from_payload(payload)

            # Read and process the CSV
            df = pd.read_csv(file_path, dtype={
                'Date': str,
                'Username': str,
                'Email': str,
                'Status': str,
                'Result': str,
                'Agent': str,
                'Name': str,
                'User Rating': str  # Treat as string initially
            })

            # Process each row
            for index, row in df.iterrows():
                try:
                    # Parse the evaluation result
                    evaluation_data = self.parse_evaluation_result(str(row['Result']))

                    # Validate and convert date to MM/DD/YYYY
                    date_str = row.get('Date', None)
                    formatted_date = None
                    if date_str and date_str.strip():
                        try:
                            # Extract only the date portion and format as MM/DD/YYYY
                            date_obj = datetime.strptime(date_str.strip().split(" - ")[0], '%b %d %Y')
                            formatted_date = date_obj.strftime('%Y-%m-%d')
                        except ValueError as ve:
                            self.ctx.logger.error(f"Invalid date format in '{date_str}' at row {index}: {ve}")
                            continue

                    # Validate and convert user rating
                    user_rating_str = row.get('User Rating', None)
                    user_rating = None
                    if user_rating_str and user_rating_str.strip().upper() != 'N/A':
                        try:
                            user_rating = float(user_rating_str.strip())
                        except ValueError:
                            self.ctx.logger.error(f"Invalid user rating '{user_rating_str}' at row {index}")
                            user_rating = None

                    status_raw = str(row['Status']).strip() if pd.notna(row['Status']) else None
                    status_value = "Passed" if "Passed" in status_raw else "Pending"

                    fields_to_add = {
                        "date": formatted_date.strip() if formatted_date else None,
                        "username": str(row['Username']).strip() if pd.notna(row['Username']) else None,
                        "email": str(row['Email']).strip() if pd.notna(row['Email']) else None,
                        "status": "Passed",
                        # "agent_name": str(payload["uploaded_by"][0]["name"]).strip(),
                        # "trainer_name": str(payload["uploaded_by"][0]["name"]).strip(),
                        "name": str(row['Name']).strip() if pd.notna(row['Name']) else None,
                        "final_score": int(evaluation_data['final_score']) if evaluation_data['final_score'] is not None else 0,
                        "engagement_score": int(evaluation_data['engagement']) if evaluation_data['engagement'] is not None else 0,
                        "knowledge_score": int(evaluation_data['knowledge']) if evaluation_data['knowledge'] is not None else 0,
                        "critical_thinking_score": int(evaluation_data['critical_thinking']) if evaluation_data['critical_thinking'] is not None else 0,
                        "minigame_score": int(evaluation_data['minigame_score']) if evaluation_data['minigame_score'] is not None else 0,
                        # "parent_record_id": payload['record_id'],
                        # "file": [{
                        #     "file_token": payload["file"][0]["file_token"],
                        #     "name": payload["file"][0]["name"]
                        # }],
                        "user_rating": float(user_rating) if user_rating is not None else 0.0
                    }



                    # Final validation for required fields
                    required_fields = ["date", "username", "email", "status", "name", "final_score"]
                    missing_fields = [field for field in required_fields if fields_to_add.get(field) is None]
                    if missing_fields:
                        self.ctx.logger.error(f"❌ Missing required fields in row {index}: {missing_fields}")
                        continue

                    # Log the fields being sent to Lark
                    self.ctx.logger.info(f"Attempting to create record with fields: {fields_to_add}")

                    # Push to processed table
                    try:
                        self.ctx.base_manager.create_record(
                            table_id=os.getenv('PROCESSED_TABLE_ID'),
                            fields=fields_to_add
                        )
                    except Exception as api_err:
                        self.ctx.logger.error(f"❌ API Error for row {index}: {api_err}")
                        self.ctx.logger.error(f"❌ Problematic fields: {fields_to_add}")

                except Exception as row_err:
                    self.ctx.logger.error(f"❌ Error processing row {index}: {row_err}")

            # Update unprocessed table record
            self.ctx.base_manager.update_record(
                table_id=os.getenv('UNPROCESSED_TABLE_ID'),
                record_id=payload['record_id'],
                fields={"status": 'done'}
            )

            self.ctx.logger.info("✅ All trainee evaluations processed.")

        except Exception as e:
            self.ctx.logger.error(f"❌ Error during trainee evaluation: {e}")

        finally:
            if 'file_path' in locals() and os.path.exists(file_path):
                delete_file(file_path)
            self.ctx.logger.info("✅ Finished trainee evaluation.")