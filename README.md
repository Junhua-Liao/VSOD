## A Video Shot Occlusion Detection Algorithm Based on the Abnormal Fluctuation of Depth Information

This repository contains the code and datasets for our [paper](https://junhua-liao.github.io/Junhua-Liao/publications/papers/TCSVT_2023.pdf) (TCSVT 2023):

> A Video Shot Occlusion Detection Algorithm Based on the Abnormal Fluctuation of Depth Information  
> Junhua Liao, Haihan Duan, Wanbing Zhao, Kanghui Feng, Yanbing Yang, Liangyin Chen

***
### Related Works
- Occlusion Detection for Automatic Video Editing (**ACM MM 2020**)
[[paper](https://junhua-liao.github.io/Junhua-Liao/publications/papers/MM_2020.pdf)]
[[project page](https://junhua-liao.github.io/Occlusion-Detection/)]
- A Light Weight Model for Video Shot Occlusion Detection (**IEEE ICASSP 2022**)
[[paper](https://junhua-liao.github.io/Junhua-Liao/publications/papers/ICASSP_2022.pdf)]
[[code](https://github.com/Junhua-Liao/ICASSP22-OcclusionDetection)]
- FLAD: A Human-centered Video Content Flaw Detection System for Meeting Recordings (**ACM NOSSDAV 2022**)
[[paper](https://junhua-liao.github.io/Junhua-Liao/publications/papers/NOSSDAV_2022.pdf)]

***
### Dataset 
- VSOD v1.0 [[project page](https://junhua-liao.github.io/Occlusion-Detection/)]
- VSOD v2.0 [[IEEE DataPort](https://dx.doi.org/10.21227/gfgt-3c35)][[Baidu Cloud](https://pan.baidu.com/s/1ahYUD3y_AkzZHQeY3uxtwg?pwd=i2u6) (i2u6)]

***
### Method
#### Data preparation
Accessing this [repository](https://github.com/isl-org/DPT), utilize **DPT-Large** to obtain the depth map of the video.

#### Testing
Set the `depth_path` in the script and execute the following code.
```
python test.py
```

***
### Citation
Please cite our papers if you use this code or datasets. 
```
@inproceedings{liao2020occlusion,
  title={Occlusion Detection for Automatic Video Editing},
  author={Liao, Junhua and Duan, Haihan and Li, Xin and Xu, Haoran and Yang, Yanbing and Cai, Wei and Chen, Yanru and Chen, Liangyin},
  booktitle={Proceedings of the 28th ACM International Conference on Multimedia},
  pages={2255--2263},
  year={2020}
}
```
```
@ARTICLE{10182309,
  author={Liao, Junhua and Duan, Haihan and Zhao, Wanbing and Feng, Kanghui and Yang, Yanbing and Chen, Liangyin},
  journal={IEEE Transactions on Circuits and Systems for Video Technology}, 
  title={A Video Shot Occlusion Detection Algorithm Based on the Abnormal Fluctuation of Depth Information}, 
  year={2023},
  volume={},
  number={},
  pages={1-1},
  doi={10.1109/TCSVT.2023.3295243}}
```

***
### Acknowledgments
Thanks for the support of the open-source repository ([DPT](https://github.com/isl-org/DPT), [NeWCRFs](https://github.com/aliyun/NeWCRFs), [GuidedDecoding](https://github.com/mic-rud/GuidedDecoding), [Jun et al.](https://github.com/jyjunmcl/Depth-Map-Decomposition)) for this research.

