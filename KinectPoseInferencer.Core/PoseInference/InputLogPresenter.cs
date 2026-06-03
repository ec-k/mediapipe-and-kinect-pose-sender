using KinectPoseInferencer.Core.InputHook;
using R3;


namespace KinectPoseInferencer.Core.PoseInference;

public class InputLogPresenter : IDisposable
{
    readonly InputEventSender _sender;
    readonly RecordDataBroker _recordDataBroker;

    DisposableBag _disposables = new();

    // Throttling for mouse events (~60fps)
    readonly TimeSpan _mouseThrottleInterval = TimeSpan.FromMilliseconds(16);
    readonly Subject<MouseEventData> _mouseEventSubject = new();

    public InputLogPresenter(
        InputEventSender sender,
        RecordDataBroker recordDataBroker)
    {
        _sender = sender ?? throw new ArgumentNullException(nameof(sender));
        _recordDataBroker = recordDataBroker ?? throw new ArgumentNullException(nameof(recordDataBroker));

        _recordDataBroker.DeviceInputData
            .Where(inputEvent => inputEvent is not null)
            .Subscribe(inputEvent =>
            {
                _sender?.SendMessage(inputEvent);
            })
            .AddTo(ref _disposables);

        // Throttle mouse events to ~60fps
        _mouseEventSubject
            .ThrottleLast(_mouseThrottleInterval)
            .Subscribe(SendMouseEvent)
            .AddTo(ref _disposables);

        GlobalInputHook.OnKeyboardEvent += KeyboardInputEventCallback;
        GlobalInputHook.OnMouseEvent += MouseInputEventCallback;
    }

    void KeyboardInputEventCallback(KeyboardEventData keyInputEvent)
    {
        var deviceInputData = new DeviceInputData
        {
            Timestamp = TimeSpan.FromTicks(keyInputEvent.RawStopwatchTimestamp),
            Data = keyInputEvent
        };

        _recordDataBroker.SetDeviceInputData(deviceInputData);
    }

    void MouseInputEventCallback(MouseEventData mouseInputEvent)
    {
        _mouseEventSubject.OnNext(mouseInputEvent);
    }

    void SendMouseEvent(MouseEventData mouseInputEvent)
    {
        var deviceInputData = new DeviceInputData
        {
            Timestamp = TimeSpan.FromTicks(mouseInputEvent.RawStopwatchTimestamp),
            Data = mouseInputEvent
        };

        _recordDataBroker.SetDeviceInputData(deviceInputData);
    }

    public void Dispose()
    {
        GlobalInputHook.OnKeyboardEvent -= KeyboardInputEventCallback;
        GlobalInputHook.OnMouseEvent -= MouseInputEventCallback;

        _mouseEventSubject.Dispose();
        _disposables.Dispose();
    }
}
