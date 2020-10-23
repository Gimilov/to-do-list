from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import calendar

weekdays = list(calendar.day_name)
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

    @staticmethod
    def print_goals(days_ahead=None):
        rows = session.query(Table).all()
        if days_ahead == 'today':
            print(f"Today {datetime.today().day} {datetime.today().strftime('%b')}")
            if len(rows) == 0:
                print('Nothing to do!')
            elif len(rows) >= 1:
                numerator = 0
                for goal in rows:
                    numerator += 1
                    print(f"{numerator}. {goal.task}. {goal.deadline.strftime('%d %b')}")
        elif days_ahead == 'week':
            for n in range(7):
                current_day = datetime.today() + timedelta(days=n)
                rows = session.query(Table).filter(Table.deadline == current_day.date()).all()
                print(f"\n{weekdays[current_day.weekday()]} {current_day.day} {current_day.strftime('%b')}:")
                if len(rows) == 0:
                    print('Nothing to do!')
                else:
                    numerator = 0
                    for goal in rows:
                        numerator += 1
                        print(f"{numerator}. {goal.task}. {goal.deadline.strftime('%d %b')}")

        elif days_ahead == 'all':  # to obtain a separate instance
            rows = session.query(Table).order_by(Table.deadline).all()
            numerator = 0
            print('All tasks:')
            for goal in rows:
                numerator += 1
                print(f"{numerator}. {goal.task}. {goal.deadline.strftime('%d %b')}")
        elif days_ahead == 'missed':
            rows = session.query(Table).filter(Table.deadline < datetime.today().date())\
                .order_by(Table.deadline).all()
            if len(rows) == 0:
                print('Nothing is missed!')
            elif len(rows) >= 1:
                numerator = 0
                print('\nMissed tasks:')
                for goal in rows:
                    numerator += 1
                    print(f"{numerator}. {goal.task}. {goal.deadline.strftime('%d %b')}")

    def menu(self):
        decision = ''  # to access the loop
        while decision != '0':
            print("""\n1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
            decision = input()
            if decision == '1':
                self.print_goals('today')
            elif decision == '2':
                self.print_goals('week')
            elif decision == '3':
                self.print_goals('all')
            elif decision == '4':
                self.print_goals('missed')
            elif decision == '5':
                the_task = input('\nEnter task: \n')
                task_deadline = input('\nEnter deadline:\n')
                task_deadline = datetime.strptime(task_deadline, "%Y-%m-%d")
                new_row = Table(task=the_task, deadline=task_deadline)
                session.add(new_row)
                session.commit()
                print('\nThe task has been added!\n')
            elif decision == '6':
                rows = session.query(Table).order_by(Table.deadline).all()
                numerator = 0
                print('\nChoose the number of the task you want to delete:')
                for goal in rows:
                    numerator += 1
                    print(f"{numerator}. {goal.task}. {goal.deadline.strftime('%d %b')}")
                no_of_row_to_delete = int(input())
                if len(rows) == 0:
                    print('Nothing to delete')
                elif len(rows) >= 1:
                    row_delete = rows[no_of_row_to_delete - 1]
                    session.delete(row_delete)
                    session.commit()
                    print("The task has been deleted!")
            elif decision == '0':
                print('\nBye!')


Base.metadata.create_all(engine)
to_do_list = Table()
to_do_list.menu()
