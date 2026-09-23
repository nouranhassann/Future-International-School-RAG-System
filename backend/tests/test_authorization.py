from app.services.authorization import get_allowed_access_levels, is_access_allowed

def test_student_access():
    levels = get_allowed_access_levels('student')
    assert 'student' in levels
    assert 'shared' in levels
    assert 'teacher' not in levels
    
    assert is_access_allowed('student', 'shared') is True
    assert is_access_allowed('student', 'student') is True
    assert is_access_allowed('student', 'teacher') is False

def test_teacher_access():
    levels = get_allowed_access_levels('teacher')
    assert 'student' in levels
    assert 'shared' in levels
    assert 'teacher' in levels
    
    assert is_access_allowed('teacher', 'teacher') is True
    assert is_access_allowed('teacher', 'student') is True
