"""
Serialization and deserialization functions for employee and department entities,
this module defines the following functions:
- DepartmentService which is department serialization and deserialization schema
"""
def emp_to_json(employee):
    """
    Serializes employee into json format data
    :param emp_object: given employee
    :return: employee in json format
    """
    e_dict = {
              "age": employee.age,
              "uuid": employee.uuid,
              "name": employee.name,
              "birth_date": employee.birth_date.strftime('%Y-%m-%d'),
              "salary": employee.salary
              }
    if employee.department:
        e_dict["department"] = employee.department.name
        e_dict["department_uuid"] = employee.department.uuid
    else:
        e_dict.setdefault('department', 'Not added')
        e_dict.setdefault('department_uuid', 'Not added')
    return e_dict


def dep_to_json(department):
    """
    Serializes department into json format data
    :param dep_object: given department
    :return: department in json format
    """
    d_dict = {
                "description": department.description,
                "uuid": department.uuid,
                "name": department.name,
                "employees": department.employees
             }
    if department.employees:
        d_dict['employees'] = [emp_to_json(emp) for emp in department.employees]
        d_dict["employees_average_age"] = sum([emp.age for emp in department.employees]) \
                                            / len(department.employees)
        d_dict["average_salary"] = sum([emp.salary for emp in department.employees]) \
                                     / len(department.employees)
        d_dict["employees_count"] = len(department.employees)
    else:
        d_dict.setdefault("employees_average_age", 0)
        d_dict.setdefault("average_salary", 0)
        d_dict.setdefault("employees_count", 0)
    return d_dict
