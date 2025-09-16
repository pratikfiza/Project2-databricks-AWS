# 🎥 YouTube Data Engineering Project (AWS + Databricks)

![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazon-aws&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-BigData-red?logo=databricks)
![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![PySpark](https://img.shields.io/badge/PySpark-ETL-yellow?logo=apachespark)

## 📌 Project Overview

This project demonstrates a **real-world cloud data pipeline** built using **AWS Services** and **Databricks** to process YouTube data at scale.

We implemented a **modern data lakehouse architecture** with **Bronze → Silver → Gold layers** powered by **Delta Lake** and orchestrated with **AWS Step Functions**.

The pipeline ingests YouTube metadata, stores raw data in S3, processes & optimizes it in Databricks, and exposes curated datasets for analytics.

---

## 🚀 Architecture Diagram

![Architecture](./docs/architecture.png)

**Workflow:**
1. **Ingestion** → AWS Lambda fetches YouTube API data, streams via Kinesis, stores raw JSON in S3.  
2. **Raw Data Storage (Bronze)** → Lambda saves ingested data in Delta format.  
3. **Orchestration** → AWS Step Functions triggers Databricks ETL job via REST API.  
4. **Transformation (Silver)** → Databricks cleans & flattens JSON, applies partitioning, and stores optimized Delta tables.  
5. **Optimizations** → Delta Lake schema evolution, Z-Ordering, VACUUM.  
6. **Analytics (Gold)** → Aggregations for reporting, dashboards, and queries via Databricks SQL / Athena.  
7. **Monitoring** → CloudWatch + SNS for alerts & job monitoring.  

---

## 📂 Project Structure

youtube-databricks-pipeline/
├── README.md
├── infra/
│ ├── main.tf # Terraform infra
│ ├── variables.tf
│ ├── outputs.tf
│ └── iam_policies.tf
├── lambda/
│ ├── ingest_preprocess/
│ ├── kinesis_consumer/
│ ├── fetch_youtube_batch/
│ └── trigger_databricks_job/
├── databricks/
│ ├── notebooks/
│ │ ├── 01_ingest_raw.py
│ │ ├── 02_transform_delta.py
│ │ ├── 03_optimizations.py
│ │ └── 04_reporting_queries.py
│ ├── jobs/
│ │ └── youtube_etl_job.json
├── stepfunctions/
│ └── state_machine.asl.json
├── cicd/
│ └── github-actions.yml
└── docs/
└── architecture.png

yaml
Copy code

---

## ⚙️ Technologies Used

- **AWS**
  - Lambda (serverless ingestion, Databricks trigger)
  - Kinesis Streams (real-time data ingestion)
  - S3 (data lake storage: raw/bronze/silver/gold)
  - DynamoDB (metadata storage)
  - Step Functions (orchestration)
  - SNS + CloudWatch (monitoring & notifications)

- **Databricks**
  - PySpark for ETL & data transformations
  - Delta Lake (schema evolution, Z-Order, VACUUM, Time Travel)
  - Databricks REST API (job triggers)
  - Databricks SQL (reporting queries)

- **Other**
  - Terraform (infra as code)
  - GitHub Actions (CI/CD)

---

## 🔨 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/youtube-databricks-pipeline.git
cd youtube-databricks-pipeline
2. Deploy Infrastructure
bash
Copy code
cd infra
terraform init
terraform apply
3. Deploy Lambda Functions
Each Lambda folder (lambda/ingest_preprocess, lambda/kinesis_consumer, etc.) has its own requirements.txt. Package and deploy:

bash
Copy code
cd lambda/ingest_preprocess
pip install -r requirements.txt -t .
zip -r function.zip .
aws lambda update-function-code --function-name ingest_preprocess --zip-file fileb://function.zip
4. Import Databricks Notebooks
Go to Databricks Workspace → Repos → Import each notebook from databricks/notebooks/.

5. Create Databricks Job
Use databricks/jobs/youtube_etl_job.json to create the job via API or UI.

6. Configure Step Functions
Upload stepfunctions/state_machine.asl.json into AWS Step Functions.

Link with Lambda for Databricks job trigger.

📊 Example Queries (Databricks SQL)
sql
Copy code
-- Top 10 Channels by Video Count
SELECT channel, COUNT(*) AS video_count
FROM youtube_silver
GROUP BY channel
ORDER BY video_count DESC
LIMIT 10;

-- Trending Videos by Month
SELECT year, month, COUNT(video_id) AS videos
FROM youtube_silver
GROUP BY year, month
ORDER BY year DESC, month DESC;
✅ Key Features
End-to-end serverless pipeline with AWS + Databricks.

Bronze → Silver → Gold data lakehouse architecture.

Delta Lake optimizations (Z-Order, schema evolution, vacuum).

Step Functions orchestration with retries & alerts.

Scalable & cloud-native design.

Analytics ready datasets.

📌 Future Improvements
Add CI/CD with Databricks Repos.

Implement real-time dashboards using Amazon QuickSight.

Add CDC (Change Data Capture) for incremental updates.

Integrate dbt for transformation lineage.

🧑‍💻 Author
Pratik Pattanaik
Cloud & Data Engineer | AWS | Databricks | PySpark | SQL
