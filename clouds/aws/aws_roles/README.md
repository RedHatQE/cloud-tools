## AWS Roles

This repository manages IAM roles and role-policies with [Boto3 IAM client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html).


An `IAM role` is an IAM identity that you can create in your account that has specific permissions.

We will create a `role policy` in AWS by creating policies and attaching them to IAM identities.

`IAM policies` define permissions for an action regardless of the method that you use to perform the operation.
Most policies are stored in AWS as JSON documents

##  Using `rhoam_add_role_policy.py`:
Required when installing RHOAM addon on a ROSA cluster.

Files implements and follows [this](https://access.redhat.com/documentation/en-us/red_hat_openshift_api_management/1/guide/53dfb804-2038-4545-b917-2cb01a09ef98#_96b0afed-7c60-4930-839a-491bbde72990:~:text=Adding%20OpenShift%20API%20Management%20to%20your%20STS%20enabled%20Red%20Hat%20OpenShift%20Service%20on%20AWS%20cluster,-Red%20Hat%20OpenShift) document.



By using the policy specified in `rhoam-sre-support-policy.json`, we will create a specific addon support for installation.

Use `poetry run aws/aws_roles/aws_roles.py` to execute the procedure.
