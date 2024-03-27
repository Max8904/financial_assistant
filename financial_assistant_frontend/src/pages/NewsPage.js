import React from 'react'
import {
  useParams
} from 'react-router-dom'
import newsList from '../assets/data'

const NewsPage = (props) => {
  let newsId = useParams().id
  let news = newsList.find(news => news.id === Number(newsId))
  return (
    <div>
        <p>{news?.body}</p>
    </div>
  )
}

export default NewsPage