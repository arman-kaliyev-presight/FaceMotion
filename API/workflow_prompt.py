
params = {
    "2": {
        "inputs": {
            "lip_zero": False,
            "lip_zero_threshold": 0.03,
            "stitching": True,
            "delta_multiplier": 1,
            "mismatch_method": "constant",
            "relative_motion_mode": "relative",
            "driving_smooth_observation_variance": 0.000003,
            "expression_friendly": False,
            "expression_friendly_multiplier": 1,
            "pipeline": [
                "3",
                0
            ],
            "crop_info": [
                "9",
                1
            ],
            "source_image": [
                "9",
                0
            ],
            "driving_images": [
                "5",
                0
            ]
        },
        "class_type": "LivePortraitProcess",
        "_meta": {
            "title": "LivePortrait Process"
        }
    },
    "3": {
        "inputs": {
            "precision": "auto",
            "mode": "human"
        },
        "class_type": "DownloadAndLoadLivePortraitModels",
        "_meta": {
            "title": "(Down)Load LivePortraitModels"
        }
    },
    "4": {
        "inputs": {
            "image": "homepage_banner_m.jpg",
            "upload": "image"
        },
        "class_type": "LoadImage",
        "_meta": {
            "title": "Load Image"
        }
    },
    "5": {
        "inputs": {
            "video": "d0.mp4",
            "force_rate": 0,
            "force_size": "Disabled",
            "custom_width": 512,
            "custom_height": 512,
            "frame_load_cap": 0,
            "skip_first_frames": 0,
            "select_every_nth": 1
        },
        "class_type": "VHS_LoadVideo",
        "_meta": {
            "title": "Load Video (Upload) 🎥🅥🅗🅢"
        }
    },
    "9": {
        "inputs": {
            "dsize": 512,
            "scale": 2.3,
            "vx_ratio": 0,
            "vy_ratio": -0.125,
            "face_index": 0,
            "face_index_order": "large-small",
            "rotate": True,
            "pipeline": [
                "3",
                0
            ],
            "cropper": [
                "10",
                0
            ],
            "source_image": [
                "4",
                0
            ]
        },
        "class_type": "LivePortraitCropper",
        "_meta": {
            "title": "LivePortrait Cropper"
        }
    },
    "10": {
        "inputs": {
            "onnx_device": "CPU",
            "keep_model_loaded": True,
            "detection_threshold": 0.5
        },
        "class_type": "LivePortraitLoadCropper",
        "_meta": {
            "title": "LivePortrait Load InsightFaceCropper"
        }
    },
    "12": {
        "inputs": {
            "frame_rate": 24,
            "loop_count": 0,
            "filename_prefix": "Generated_Video",
            "format": "video/h264-mp4",
            "pix_fmt": "yuv420p",
            "crf": 19,
            "save_metadata": True,
            "pingpong": False,
            "save_output": True,
            "images": [
                "2",
                0
            ]
        },
        "class_type": "VHS_VideoCombine",
        "_meta": {
            "title": "Video Combine"
        }
    }
}
