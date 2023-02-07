resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.dataset_id 
}

resource "google_bigquery_dataset_iam_binding" "reader" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  role       = "roles/bigquery.dataViewer"

  members = var.users
}

