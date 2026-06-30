namespace KinectPoseInferencer.RemoteControl;

public record RemoteControlOptions
{
    public const string SectionName = "RemoteControl";
    public int Port { get; set; } = 8080;
    public bool AllowRemoteAccess { get; set; } = false;
}
