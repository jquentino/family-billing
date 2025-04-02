# Family Billing Microservice

This project is a microservice designed to charge family members who have made purchases on your credit card. It is developed to run as a cloud function on Google Cloud Platform (GCP).

---

## Running the Family Billing Microservice Locally

This guide explains how to run the `Family Billing Microservice` locally using the `functions-framework` package.

---

### Prerequisites

1. **Python Installed**: Ensure Python 3.9 or higher is installed on your system.
2. **Install Dependencies**: While this project does not require dependencies for running on Cloud Run, you will need to install `functions-framework` and `Flask` to run it locally.

---

### Steps to Run Locally

#### 1. Install Dependencies

Navigate to the project directory and install the dependencies listed in `requirements.txt`. It is recommended to use a virtual environment instead of global pip.

```bash
pip install -r requirements.txt
```

#### 2. Set Environment Variables

The microservice relies on the following environment variables:

- `APP_EMAIL_ADDRESS`: Your email address (e.g., `your_email@gmail.com`).
- `APP_EMAIL_PASSWORD`: Your email password or app-specific password.
- `PIX_KEY`: Your PIX key for payment.

Set these variables in your terminal. For example, on Windows:

```bash
set APP_EMAIL_ADDRESS=your_email@gmail.com
set APP_EMAIL_PASSWORD=your_password
set PIX_KEY=your_pix_key
```

Alternatively, you can create a `.env` file in the project directory and use a library like `python-dotenv` to load the variables.

#### 3. Run the Microservice

Use the `functions-framework` command to start the service locally:

```bash
functions-framework --target send_email --debug
```

#### 4. Test the Service

Once the service is running, you can test it by sending a POST request to `http://localhost:8080` using a tool like `curl` or Postman. For example:

Using `curl`:

```bash
curl -X POST http://localhost:8080 \
-H "Content-Type: application/json" \
-d '{
    "recievers": [
        {
            "name": "John Doe",
            "emails": ["john.doe@example.com"],
            "items": ["item1", "item2"],
            "value": "100.00"
        }
    ]
}'
```

---

## Deploying the Microservice to Cloud Run

### 1. Fork the Project

To deploy using continuous integration with GitHub, create a fork of this project in your GitHub account.

### 2. Prepare Your Environment

Ensure the following:

- Your project is set up in Google Cloud.
- Billing is enabled for the project.
- The Cloud Run API is enabled.

### 3. Deploy Using the Cloud Run Interface

Since this service is simple and has minimal dependencies, the easiest way to deploy it is through the Cloud Run interface. Follow these steps:

1. Go to the [Cloud Run Console](https://console.cloud.google.com/run).
2. Click **Deploy Container**.
3. Select **Service**.
4. Choose the **GitHub** option.
5. Click **Configure with Cloud Build** and follow the instructions to connect your GitHub forked repository with Cloud Run.
6. Under **Service Name**, enter `family-billing` or another name of your choice.
7. Ensure the option **Use Cloud IAM to authenticate incoming requests** is selected.
8. Under the **Edit Container** pane, go to **Variables and Secrets** and add the environment variables discussed earlier.
9. Click **Create**.

---

## Scheduling a Cron Job with Cloud Scheduler

This guide explains how to schedule a cron job to trigger the `Family Billing Microservice` periodically using **Google Cloud Scheduler**.

---

### Prerequisites

1. **Deployed Microservice**: Ensure the microservice is already deployed to **Google Cloud Run** and accessible via a public or private URL.
2. **Cloud Scheduler API Enabled**: Enable the **Cloud Scheduler API** in your Google Cloud project:
   - Go to the [Cloud Scheduler API](https://console.cloud.google.com/apis/library/cloudscheduler.googleapis.com).
   - Click **Enable**.

---

### Steps to Schedule the Cron Job

#### 1. Open Cloud Scheduler

1. Go to the [Cloud Scheduler Console](https://console.cloud.google.com/cloudscheduler).
2. Click **Create Job**.

#### 2. Configure the Job

1. **Name**: Enter a name for the job (e.g., `family-billing-cron`).
2. **Frequency**: Set the frequency using a cron expression. Examples:
   - `0 9 * * *`: Runs every day at 9:00 AM.
   - `0 0 1 * *`: Runs on the first day of every month at midnight.
   - Use [cron syntax](https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules) for custom schedules.
3. **Timezone**: Select your preferred timezone.

#### 3. Set the Target

1. **Target Type**: Select **HTTP**.
2. **URL**: Enter the URL of your deployed Cloud Run service (e.g., `https://[REGION]-[PROJECT_ID].run.app`).
3. **HTTP Method**: Select **POST**.
4. **Body**: Add the JSON payload that the microservice expects. For example:

   ```json
   {
       "recievers": [
           {
               "name": "John Doe",
               "emails": ["john.doe@example.com"],
               "items": ["item1", "item2"],
               "value": "100.00"
           }
       ]
   }
   ```

#### 4. Authentication

1. **Authentication Header**: Select **Add OIDC Token**.
2. **Service Account**: Use the default service account or select a custom service account with the necessary permissions to invoke the Cloud Run service.

#### 5. Create the Job

1. Review the configuration.
2. Click **Create** to save and schedule the job.

#### 6. Testing the Cron Job

1. In the Cloud Scheduler Console, locate your job.
2. Click **Run Now** to test the job manually.

