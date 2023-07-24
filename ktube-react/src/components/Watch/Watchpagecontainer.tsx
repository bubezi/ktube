import Channeldetails from "./Channeldetails";
import Likeanddislike from "./Likeanddislike";

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
        />
      </div>
      <Likeanddislike videoId={props.videoId} likes={props.likes} dislikes={props.dislikes}/>
    </>
  );
}
