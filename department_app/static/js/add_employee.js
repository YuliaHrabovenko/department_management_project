/**
 * Helper function for POSTing data as JSON with fetch.
 *
 * @param {Object} options
 * @param {string} options.url - URL to POST data to
 * @param {FormData} options.formData - form data values
 * @return {Object} - Response body from URL that was POSTed to
 */
async function postFormDataAsJson({ url, formData }) {
    const formDataJsonString = JSON.stringify(formData);

    const fetchOptions = {
        /**
         * The default method for a request with fetch is GET,
         * that uses the POST HTTP method.
         */
        method: "POST",
        /**
         * These headers will be added to the request and tell
         * the API that the request body is JSON and that we can
         * accept JSON responses.
         */
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        /**
         * The body of our POST request is the JSON string
         * created above.
         */
        body: formDataJsonString,
    };

    const response = await fetch(url, fetchOptions);

    if (!response.ok) {
        const errorMessage = await response.text();
        throw new Error(errorMessage);
    }

    return response.json();
}
/**
 * Event handler for a form submit event.
 *
 * @param {SubmitEvent} event
 */
async function handleFormSubmit(event) {
    /**
     * This prevents the default behaviour of the browser submitting
     * the form so that we can handle things instead.
     */
    event.preventDefault();
    /**
     * Inserting form data values into formData dictionary
     */
    const formData = {};
    formData['name'] = document.getElementById('name').value;
    formData['birth_date'] = document.getElementById('birth_date').value;
    formData['salary'] = document.getElementById('salary').value;
    var department_uuid = document.getElementById('department').value;

    if (!formData['name'].replace(/\s/g, '').length) {
       document.getElementById('name_error').innerHTML = 'Invalid employee name.';
    }

    /**
     * This holds the API URL.
     */
    const url = `/api/employees?department_uuid=${department_uuid}`

    try {
        const responseData = await postFormDataAsJson({ url, formData });
        location.replace("/employees")

    } catch (error) {
        console.error(error);
    }
}

const formAddEmp = document.getElementById("addEmpForm");
formAddEmp.addEventListener("submit", handleFormSubmit);