# Packaging Google Cloud Python clients for Fedora

Fedora RPM packaging for [Google Cloud's Python clients]. This is a work in
progress.

Want to test these now? Take a look at my [python-google COPR repositories].

[Google Cloud's Python clients]: https://github.com/googleapis/google-cloud-python
[python-google COPR repositories]: https://copr.fedorainfracloud.org/coprs/mhayden/python-google-cloud/


## In progress

| Client | Status | Notes |
| ------ | ------ | ----- |
| AI Platform | 🔴 | Requires Bigquery which has no Python 3.10 support |
| Bigquery | 🔴 | No Python 3.10 support |
| Functions | 🟡 | In review |
| KMS | 🟡 | In review, requires grpc-google-iam-v1 + pem |
| Redis | 🟡 | In review |


## Completed

| Client | Status | Notes |
| ------ | ------ | ----- |
| IAM | 🟢 | |
| Storage | 🟢 | |
