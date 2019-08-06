from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from AR.PG.tables.user_profile import UserProfile
from AR.PG.tables.learning_plan import LearningPlan
from AR.PG.tables.activity import Activity
from AR.PG.tables.activity_format import ActivityFormat
from AR.PG.tables.goal import Goal
from AR.PG.tables.activity_objective import ActivityObjective
