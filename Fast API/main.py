from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

# Instancia o FastAPI
app = FastAPI()

# Configuração do banco de dados
SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://root:Ps813898@localhost:3306/prova9'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
Base = declarative_base()

# Modelos
class Job(Base):
    __tablename__ = "jobs"
    JobID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(255))
    Description = Column(String(255))
    employees = relationship("Employee")


class Employee(Base):
    __tablename__ = "employees"
    EmployeeID = Column(Integer, primary_key=True, index=True)
    E_JobID = Column(Integer, ForeignKey('jobs.JobID'))
    Name = Column(String(255))
    Birthday = Column(String(255))
    Salary = Column(Float())
    Department = Column(String(255))
    job = relationship("Job")
    job_history = relationship("JobHistory")

class JobHistory(Base):
    __tablename__ = "job_history"
    JobHistoryID = Column(Integer, primary_key=True, index=True)
    E_EmployeeID = Column(Integer, ForeignKey('employees.EmployeeID'))
    Title = Column(String(255))
    StartDate = Column(String(255))
    EndDate = Column(String(255))
    Salary = Column(Float())
    Job = Column(String(255))
    employee = relationship("Employee",)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Rotas para Job
@app.get("/api/jobs")
def read_jobs():
    jobs = session.query(Job).all()
    return JSONResponse(content=[{"JobID": job.JobID, "Name": job.Name, "Description": job.Description} for job in jobs])

@app.post("/api/jobs")
def create_job(name: str, description: str):
    job = Job(Name=name, Description=description)
    session.add(job)
    session.commit()
    session.refresh(job)
    return JSONResponse(content={"JobID": job.JobID, "Name": job.Name, "Description": job.Description})

@app.get("/api/jobs/{job_id}")
def read_job(job_id: int):
    job = session.query(Job).filter(Job.JobID == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    employees = [{"EmployeeID": emp.EmployeeID, "Name": emp.Name} for emp in job.employees]
    return JSONResponse(content={"JobID": job.JobID, "Name": job.Name, "Description": job.Description, "Employees": employees})

@app.put("/api/jobs/{job_id}")
def update_job(job_id: int, name: str, description: str):
    job = session.query(Job).filter(Job.JobID == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.Name = name
    job.Description = description
    session.commit()
    return JSONResponse(content={"JobID": job.JobID, "Name": job.Name, "Description": job.Description})

@app.delete("/api/jobs/{job_id}")
def delete_job(job_id: int):
    job = session.query(Job).filter(Job.JobID == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    session.delete(job)
    session.commit()
    return JSONResponse(content={"JobID": job.JobID, "Name": job.Name, "Description": job.Description})

# Rotas para Employee
@app.get("/api/employees")
def read_employees():
    employees = session.query(Employee).all()
    return JSONResponse(content=[{"EmployeeID": emp.EmployeeID, "Name": emp.Name, "Birthday": str(emp.Birthday), "Salary": emp.Salary, "Department": emp.Department} for emp in employees])

@app.post("/api/employees")
def create_employee(e_job_id: int, name: str, birthday: str, salary: float, department: str):
    employee = Employee(E_JobID=e_job_id, Name=name, Birthday=birthday, Salary=salary, Department=department)
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return JSONResponse(content={"EmployeeID": employee.EmployeeID, "Name": employee.Name, "Birthday": str(employee.Birthday), "Salary": employee.Salary, "Department": employee.Department})

@app.get("/api/employees/{employee_id}")
def read_employee(employee_id: int):
    employee = session.query(Employee).filter(Employee.EmployeeID == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    job_histories = [{"JobHistoryID": jh.JobHistoryID, "Title": jh.Title} for jh in employee.job_history]
    return JSONResponse(content={"EmployeeID": employee.EmployeeID, "Name": employee.Name, "Birthday": str(employee.Birthday), "Salary": employee.Salary, "Department": employee.Department, "JobHistories": job_histories})

@app.put("/api/employees/{employee_id}")
def update_employee(employee_id: int, e_job_id: int, name: str, birthday: str, salary: float, department: str):
    employee = session.query(Employee).filter(Employee.EmployeeID == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee.E_JobID = e_job_id
    employee.Name = name
    employee.Birthday = birthday
    employee.Salary = salary
    employee.Department = department
    session.commit()
    return JSONResponse(content={"EmployeeID": employee.EmployeeID, "Name": employee.Name, "Birthday": str(employee.Birthday), "Salary": employee.Salary, "Department": employee.Department})

@app.delete("/api/employees/{employee_id}")
def delete_employee(employee_id: int):
    employee = session.query(Employee).filter(Employee.EmployeeID == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    session.delete(employee)
    session.commit()
    return JSONResponse(content={"EmployeeID": employee.EmployeeID, "Name": employee.Name, "Birthday": str(employee.Birthday), "Salary": employee.Salary, "Department": employee.Department})

# Rotas para JobHistory
@app.get("/api/job_history")
def read_job_histories():
    job_histories = session.query(JobHistory).all()
    return JSONResponse(content=[{"JobHistoryID": jh.JobHistoryID, "Title": jh.Title, "StartDate": str(jh.StartDate), "EndDate": str(jh.EndDate), "Salary": jh.Salary, "Job": jh.Job} for jh in job_histories])

@app.post("/api/job_history")
def create_job_history(e_employee_id: int, title: str, start_date: str, end_date: str, salary: float, job: str):
    job_history = JobHistory(E_EmployeeID=e_employee_id, Title=title, StartDate=start_date, EndDate=end_date, Salary=salary, Job=job)
    session.add(job_history)
    session.commit()
    session.refresh(job_history)
    return JSONResponse(content={"JobHistoryID": job_history.JobHistoryID, "Title": job_history.Title, "StartDate": str(job_history.StartDate), "EndDate": str(job_history.EndDate), "Salary": job_history.Salary, "Job": job_history.Job})

@app.get("/api/job_history/{job_history_id}")
def read_job_history(job_history_id: int):
    job_history = db.query(JobHistory).filter(JobHistory.JobHistoryID == job_history_id).first()
    if not job_history:
        raise HTTPException(status_code=404, detail="Job history not found")
    return JSONResponse(content={"JobHistoryID": job_history.JobHistoryID, "Title": job_history.Title, "StartDate": str(job_history.StartDate), "EndDate": str(job_history.EndDate), "Salary": job_history.Salary, "Job": job_history.Job})

@app.put("/api/job_history/{job_history_id}")
def update_job_history(job_history_id: int, e_employee_id: int, title: str, start_date: str, end_date: str, salary: float, job: str):
    job_history = session.query(JobHistory).filter(JobHistory.JobHistoryID == job_history_id).first()
    if not job_history:
        raise HTTPException(status_code=404, detail="Job history not found")
    job_history.E_EmployeeID = e_employee_id
    job_history.Title = title
    job_history.StartDate = start_date
    job_history.EndDate = end_date
    job_history.Salary = salary
    job_history.Job = job
    session.commit()
    return JSONResponse(content={"JobHistoryID": job_history.JobHistoryID, "Title": job_history.Title, "StartDate": str(job_history.StartDate), "EndDate": str(job_history.EndDate), "Salary": job_history.Salary, "Job": job_history.Job})

@app.delete("/api/job_history/{job_history_id}")
def delete_job_history(job_history_id: int):
    job_history = session.query(JobHistory).filter(JobHistory.JobHistoryID == job_history_id).first()
    if not job_history:
        raise HTTPException(status_code=404, detail="Job history not found")
    session.delete(job_history)
    session.commit()
    return JSONResponse(content={"JobHistoryID": job_history.JobHistoryID, "Title": job_history.Title, "StartDate": str(job_history.StartDate), "EndDate": str(job_history.EndDate), "Salary": job_history.Salary, "Job": job_history.Job})