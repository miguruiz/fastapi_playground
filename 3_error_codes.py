# Error codes for the application
# 1xx -> Information response: Request is Processing. "Something is happening"
# 2xx -> Success response: Request is successful. "Everything is fine"
#        200 -> Commonly used for successful GET requests when data is returned.
#        201 -> Commonly used for successful POST requests when a new resource is created.
#        204 -> Commonly used for successful for PUT and DELETE requests when the request is successful but does not return content.
# 3xx -> Redirection response: Request is redirected. "Further action is needed"
# 4xx -> Client error response: Request contains an error. "Something is wrong with the request"
#        400 -> Bad Request: The request cannot be processed due to client error.
#        401 -> Unauthorized: The client does not have the right authorisation.
#        403 -> Forbidden: The client does not have permission to access the requested resource.
#        404 -> Not Found: The client requested resource does not exist.
#        422 -> Unprocessable Entity: The request is well-formed but contains semantic errors, such as validation errors.
# 5xx -> Server error response: Request cannot be processed. "Something went wrong on the server side"
#        500 -> Internal Server Error: Generic message when an unexpected issue on the server occurs.