import React, {useState, useEffect} from 'react'
// import newsList from '../assets/data'
import ListItem from '../components/ListItem'

const NewsListPage = () => {

  let [newsList, setNewsList] = useState([])

  useEffect(() => {
    getNews()
  }, [])

  let getNews = async () => {
    let response = await fetch('http://localhost:8000/notes')
    let data = await response.json()
    setNewsList(data)
  }

  return (
    <div className="news">
      <div className="news-header">
        <h2 className="news-title">&#9782; News</h2>
        <p className="news-count">{newsList.length}</p>
      </div>
      <div className="news-list">
        {newsList.map((news, index) => (
            <ListItem key={index} news={news}/>
        ))}
      </div>
    </div>
    
  )
}

export default NewsListPage