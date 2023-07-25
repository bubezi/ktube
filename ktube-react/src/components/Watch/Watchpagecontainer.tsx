import Channeldetails from "./Channeldetails";
import Comments from "./Comments";

interface Prop {
  title: string;
  channel: string;
  subscriber_count: number;
  private: boolean;
  unlisted: boolean;
  profile_picture: string;
  channelId: number;
  subscribers: number[],
  channelUserId: number,
  videoId: number,
  views: number,
  likes: number,
  dislikes: number,
  description: string,
  upload_time: string,
}

export default function Watchpagecontainer(props: Prop) {
  return (
    <>
      <div className="container" style={containerStyle}>
        <Channeldetails
          title={props.title}
          channel={props.channel}
          subscriber_count={props.subscriber_count}
          private={props.private}
          unlisted={props.unlisted}
          profile_picture={props.profile_picture}
          channelId={props.channelId}
          subscribers={props.subscribers}
          channelUserId={props.channelUserId}
          videoId={props.videoId}
          views={props.views}
          likes={props.likes}
          dislikes={props.dislikes}
          description={props.description}
          upload_time={props.upload_time}
        />
        <Comments videoId={props.videoId}/>
      </div>
    </>
  );
}
