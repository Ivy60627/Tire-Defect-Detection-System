import imagingcontrol4 as ic4
ic4.Library.init()
print(ic4.DeviceEnum.devices())
# Create a Grabber object
grabber = ic4.Grabber()

# Open the first available video capture device
first_device_info = ic4.DeviceEnum.devices()[0]
grabber.device_open(first_device_info)

# Set the resolution to 640x480
grabber.device_property_map.set_value(ic4.PropId.WIDTH, 4000)
grabber.device_property_map.set_value(ic4.PropId.HEIGHT, 3000)

# Create a SnapSink. A SnapSink allows grabbing single images (or image sequences) out of a data stream.
sink = ic4.SnapSink()
# Setup data stream from the video capture device to the sink and start image acquisition.
grabber.stream_setup(sink, setup_option=ic4.StreamSetupOption.ACQUISITION_START)

try:
    # Grab a single image out of the data stream.
    image = sink.snap_single(10000)

    # Print image information.
    print(f"Received an image. ImageType: {image.image_type}")

    # Save the image.
    image.save_as_bmp("test.bmp")

except ic4.IC4Exception as ex:
    print(ex.message)
	
# Stop the data stream.
grabber.stream_stop()