import React, {useState, useEffect} from 'react'
import {
  Link,
  useParams
} from 'react-router-dom'
// import newsList from '../assets/data'
import {ReactComponent as ArrowLeft} from '../assets/arrow-left.svg'


const NewsPage = (props) => {
  let newsId = useParams().id

  // let news = newsList.find(news => news.id === Number(newsId))
  let [news, setNews] = useState(null)

  useEffect(() => {
    getNews()
  }, [newsId])

  let getNews = async () => {
    let response = await fetch(`http://localhost:8000/notes/${noteId}`)
    let data = await response.json()
    setNews(data)
  }
  
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