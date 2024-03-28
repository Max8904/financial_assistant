import React from 'react'
import {
  Link,
  useParams
} from 'react-router-dom'
import newsList from '../assets/data'
import {ReactComponent as ArrowLeft} from '../assets/arrow-left.svg'


const NewsPage = (props) => {
  let newsId = useParams().id
  let news = newsList.find(news => news.id === Number(newsId))
  return (
    <div className="news">
      <div className="news-header">
        <h3>
          <Link to="/">
            <ArrowLeft />
          </Link>
        </h3>
      </div>
      <p>{news?.body}</p>
    </div>
  )
}

export default NewsPage