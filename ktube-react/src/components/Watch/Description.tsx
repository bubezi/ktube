interface Props {
  description: string;
  upload_time: string;
}

const Description = (props: Props) => {
  const DescriptionText = () => {
    if (props.description === "") {
      return (
        <div className="row">
          <h6>No Description</h6>
        </div>
      );
    } else {
      return (
        <div className="row">
          <h6>{props.description}</h6>
        </div>
      );
    }
  };

  const Uploadedon = () => {
    if (props.upload_time !== "") {
      return (
        <div className="row">
          <h6>
            Video uploaded on {props.upload_time.split("T")[0]} at{" "}
            {props.upload_time.split("T")[1].split(".")[0]}{" "}
          </h6>
        </div>
      );
    } else {
      return <></>;
    }
  };
  return (
    <>
      <div className="row box-element">
        <div className="col-lg-12">
          <div className="description">
            <h4>
              <u>Description</u>
            </h4>
            <DescriptionText />
            <hr />
            {/* <div className="row"><h6>Video uploaded {{video.upload_time | naturaltime }} on {{video.upload_time }}</h6></div> */}
            <Uploadedon />
          </div>
        </div>
      </div>
    </>
  );
};

export default Description;
