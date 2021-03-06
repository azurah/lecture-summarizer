from summarizer.tables import Lecture, Engine
from typing import List, Dict


class LectureService(object):

    def __init__(self, memory_only=False):
        self.memory_only: bool = memory_only

    def create_lecture(self, request_body: Dict[str, str]) -> Dict[str, str]:
        session = Engine.get_instance(self.memory_only).Session()
        lecture = Lecture(
            name=request_body['name'],
            course=request_body['course'],
            content=request_body['content']
        )
        session.add(lecture)
        session.flush()
        session.commit()
        return {"id": lecture.id}

    def get_lecture(self, l_id: int) -> Dict[str, str]:
        session = Engine.get_instance(self.memory_only).Session()
        query = session.query(Lecture).filter(Lecture.id == l_id)
        lecture: Lecture = query.first()
        if lecture:
            return {
                'id': lecture.id,
                'name': lecture.name,
                'course': lecture.course,
                'content': lecture.content
            }
        return {}

    def get_lectures(self, course: str, name: str, limit: int) -> List[Dict[str, str]]:
        session = Engine.get_instance(self.memory_only).Session()
        query = session.query(Lecture)
        if course:
            query = query.filter(Lecture.course == course)
        if name:
            query = query.filter(Lecture.name == name)

        limit = limit if limit else 10
        query = query.limit(limit)

        result = query.all()
        return [{
            'id': lecture.id,
            'name': lecture.name,
            'course': lecture.course,
            'content': lecture.content
        } for lecture in result]

    def delete_lecture(self, l_id: int) -> Dict[str, int]:
        session = Engine.get_instance(self.memory_only).Session()
        lecture = session.query(Lecture).filter(Lecture.id == l_id).first()
        if lecture:
            session.delete(lecture)
            session.commit()
            return {'id': l_id}
        return {}
