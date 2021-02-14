import {React} from 'react';

export function TweetList(props) {
    return (
        <div>
            {props.tweets.map((tweet) => {
                return <p>{tweet.content}</p>
            })}
        </div>
    );
}