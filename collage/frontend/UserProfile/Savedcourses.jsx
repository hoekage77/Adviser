import { Image, Button, Rating, ActionIcon } from "@mantine/core";
import { IconBookmark } from '@tabler/icons-react';
import React, {useState, useEffect} from "react";
import axios from 'axios';
import Cookies from 'js-cookie';
import '../CSS/savedCourses.css';
import courseLogo1 from '../images/tempLogo1.png';
import courseLogo2 from '../images/tempLogo2.png';
import courseLogo3 from '../images/tempLogo3.png';
import courseLogo4 from '../images/tempLogo4.png';
import '../CSS/course_tag.css';
import starFilled from '../Icons/starFilled.svg';
import starEmpty from '../Icons/starEmpty.svg';

const stars = (numStars) => {
    const starComponent = Array(5).fill(0).map((_, index) => (
    <span key={index} className="star">
      {index < numStars ? (
        <img className='star' src= {starFilled} alt="S" />
      ) : (
        <img src= {starEmpty} alt="E" />
      )}
    </span>
    ));
    return starComponent;
}

const Savedcourses = () => {
    const [courses, setCourses] = useState([])

    useEffect(() => {
        axios.get(`/api/get-saved-courses`, {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${Cookies.get('access_token')}`,
              },
        })
        .then(response => setCourses(response.data.courses))
        .catch(err => {console.error(err)});
    }, []);

    const removeSave = (course_id) => {
        axios.delete(`/api/delete-saved-course`, {
            data: {course_id}, 
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${Cookies.get('access_token')}`,
              }
        })
        .then(response => {
            console.log(response.data);
            setCourses(prevCourses => prevCourses.filter(course => course.course_id !== course_id));
        })
        .catch(err => {console.error(err)});
    };

    return (
        <ul className="courses">
            {courses.length > 0 ? courses.map((course) => (
                <li key={course.course_id}>
                    <div className="course">
                        <Image src={ course.icon_url } className="logo"></Image>
                        <div className="saved-text">
                            <p className="saved-course-title">{course.course_code}</p>
                            <p className="description">{course.course_description}</p>
                        </div>
                        <div className="rating-saved">
                            {stars(course.total_rating)}
                        </div>
                        <div className="bookmark">
                            <Button onClick={() => removeSave(course.course_id)}>Unsave</Button>
                        </div>
                    </div>
                </li>
            )) : 'No saved courses'}
        </ul>
    )
}

export default Savedcourses;
