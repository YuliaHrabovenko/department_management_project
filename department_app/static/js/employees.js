const tableBody = document.querySelector("tbody");
const dateForm = document.getElementById("dateForm");
const url = '/api/employees';
var output = '';

// Employees table visualisation
const renderEmployees = (employees) => {
    employees.forEach(employee => {
            output += `
            <tr>
                <th scope="row"></th>
                <td class="name">${employee.name}</td>
                <td class="birth_date">${employee.birth_date}</td>
                <td class="age">${employee.age} y.o</td>
                <td class="department">${employee.department}</td>
                <td class="salary">${employee.salary}$</td>
                <td class="col-md-2">
                    <div id=${employee.uuid} class='${employee.name}'>
                        <a href="/edit_employee/${employee.uuid}" onclick="redirectToEditPage();" class="btn btn-primary btn-sm align-self-center" id="edit-emp">Edit</a> |
                        <a href="" class="btn btn-danger btn-sm align-self-center" id='delete-emp'> Delete</a>
                    </div>
                </td>
            </tr>
            `;
        })
        tableBody.innerHTML = output;
}


//GET - Read the departments
//Method Get

fetch(url)
    .then(res => res.json())
    .then(data => renderEmployees(data));

const checkbox = document.getElementById('check-box');
checkbox.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        document.getElementById('end-date').disabled = true;
    } else {
        document.getElementById('end-date').disabled = false;
    }
})

// Do search by a specific date or in period between dates for employees
const submitPressed = document.getElementById('submit-btn');
async function searchByDate() {
    submitPressed.addEventListener('click', (e) => {
        e.preventDefault();
        var start = document.getElementById('start-date');
        var end = document.getElementById('end-date');

        // Search of employees born in a specific date
        if (!end.disabled){
            output = '';
            fetch(`/api/employees/search?start_date=${start.value}&end_date=${end.value}`, {
                method:'GET'
            })
            .then(res => res.json())
            .then(data => renderEmployees(data));

        }
        // Search of employees born in period between dates
        if (end.disabled){
            output = '';
            fetch(`/api/employees/search?date=${start.value}`, {
                method:'GET'
            })
            .then(res => res.json())
            .then(data => renderEmployees(data));
        }
    })
}
searchByDate();
//Modal delete window for department

// Get the modal
var modal = document.getElementById("delModal");
var pElem = document.getElementById("emp-name");

async function deleteEmployee() {
    tableBody.addEventListener('click', (e) => {
    e.preventDefault();
    let delButtonPressed = e.target.id == 'delete-emp';
    let id = e.target.parentElement.id;
    let name = e.target.parentElement.className;
    // Delete - Remove the existing department
    // method: Delete
    if(delButtonPressed){
        $('#delModal').modal('show');
        if($('.modal.show').length){
            pElem.textContent = name;
            modal.addEventListener('click', (e) => {
                let submitModalBtn = e.target.id == 'delete';
                async function fetchDelete(){
                    const response = await fetch(`${'/api/employees'}/${id}`, {
                        method: 'DELETE',
                        });
                    if (!response.ok) {
                        const message = `An error has occured: ${response.status}`;
                        throw new Error(message);
                    }
                        const result= await response.json();
                        return result;
                    }

                if(submitModalBtn){
                    fetchDelete().catch(error => {
                        error.message;
                    });
                    window.location.reload();
                }
            })
        }
    }
    })
  }

deleteEmployee();

// Redirect to edit page
function redirectToEditPage(){
    tableBody.addEventListener('click', (e) => {
    e.preventDefault();
    let uuid = e.target.parentElement.id;
    const parent = e.target.parentElement
    window.location.href = "/edit_employee/" + `${uuid}`;
})
}

// Update - Update the existing employee
// method: Update
async function editDepartment() {
    tableBody.addEventListener('click', (e) => {
    e.preventDefault();
    let editButtonPressed = e.target.id == 'edit-dep';
    let uuid = e.target.parentElement.id;
    const parent = e.target.parentElement
    window.location.href = "/edit_employee/" + `${uuid}`;
 })
}
