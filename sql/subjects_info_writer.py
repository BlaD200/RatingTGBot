from sql import initialize_connection, update_last_index
from mysql.connector.errors import DataError


def fill_subjects_info_table(subjects: list, year: int, speciality: str, faculty: str):
    """
    Accesses to :code:`subjects_info` in the database to populate table with given values

    :param subjects: list of str of contains subjects names
    :param year: year of study
    :param speciality: name of speciality
    :param faculty: name of faculty
    """
    db = initialize_connection()
    cursor = db.cursor()

    update_last_index(db, "subjects_info", "subject_id")

    for subject in subjects:
        values = (subject, year, speciality, faculty)
        # print(values, sep=',')
        for val in values:
            if not val:
                var_name = [k for k, v in locals().items() if v == val][0]
                raise ValueError('%s cannot be "%s"' % (var_name, val))
        cursor.execute(
            "SELECT subject_id from subjects_info WHERE subject_name = %s AND "
            "study_year = %s AND faculty_name = %s;", (subject, year, faculty))
        old_id = cursor.fetchall()
        try:
            if old_id:
                old_id = old_id[0][0]
                cursor.execute("INSERT INTO subjects_info VALUES"
                               "(%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE "
                               "subject_name = %s, study_year = %s, specialty = %s, faculty_name = %s",
                               (old_id, *values, *values))
            else:
                cursor.execute("INSERT INTO subjects_info(subject_name, study_year, specialty, faculty_name) VALUES"
                               "(%s, %s, %s, %s)", values)
        except DataError as e:
            print(values)
            raise DataError

        db.commit()

    db.close()


def get_faculty(timetable_name):
    """
    Access to :code:`update_info` table to get the faculty name

    :param timetable_name: filename of timetable
    :return: faculty name
    """
    db = initialize_connection()
    cursor = db.cursor()

    cursor.execute("SELECT faculty_name from update_info WHERE timetable_name = %s;", (timetable_name,))
    faculty_name = cursor.fetchone()
    db.close()

    return faculty_name[0]


def is_mp(timetable_name: str) -> bool:
    """
    Access to :code:`update_info` table to get if this is timetable for master's program

    :param timetable_name: filename of timetable
    :return: True if given timetable is for master's program else False
    """
    db = initialize_connection()
    cursor = db.cursor()

    cursor.execute("SELECT isMP FROM update_info WHERE timetable_name = %s;", (timetable_name,))
    mp = cursor.fetchone()
    db.close()

    return mp[0]
