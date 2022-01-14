const tableBody = document.querySelector("tbody");
const url = '/api/departments';
let output = '';

// Department table visualisation
const renderDepartments = (departments) => {
    departments.forEach(department => {
            output += `
            <tr>
                <th scope="row"></th>
                <td class="name">${department.name}</td>
                <td class="col-md-3 description">${department.description}</td>
                <td>${department.average_salary}$</td>
                <td>${department.employees_count}</td>
                <td>${department.employees_average_age} y.o</td>
                <td class="col-md-2">
                    <div id=${department.uuid} class='${department.name}'>
                        <a href="/edit_department/${department.uuid}" onclick="redirectToEditPage();" class="btn btn-primary btn-sm align-self-center" id="edit-dep">Edit</a> |
                        <a href="" class="btn btn-danger btn-sm align-self-center" id='delete-dep'>Delete</a>
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
    .then(data => renderDepartments(data));

//Modal delete window for department

// Get the modal
var modal = document.getElementById("delModal");
var pElem = document.getElementById("dep-name");

async function deleteDepartment() {
    tableBody.addEventListener('click', (e) => {
    e.preventDefault();
    let delButtonPressed = e.target.id == 'delete-dep';
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
                    const response = await fetch(`${'/api/departments'}/${id}`, {
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
                        error.message; // 'An error has occurred: 404'
                    });
                    window.location.reload();
                }
            })
        }
    }
    })
  }

deleteDepartment();

// Redirects to edit page
function redirectToEditPage(){
    tableBody.addEventListener('click', (e) => {
    e.preventDefault();
    let uuid = e.target.parentElement.id;
    const parent = e.target.parentElement
    window.location.href = "/edit_department/" + `${uuid}`;
})
}

// Update - Update the existing department
// method: Update
async function editDepartment() {
    tableBody.addEventListener('click', (e) => {
    e.preventDefault();
    let editButtonPressed = e.target.id == 'edit-dep';
    let uuid = e.target.parentElement.id;
    const parent = e.target.parentElement
    window.location.href = "/edit_department/" + `${uuid}`;
 })
}


