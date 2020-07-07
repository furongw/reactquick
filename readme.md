# reaction fast
一个简单的英语单词听写音频生成器。

最近在学托福，我们知道托福听力很重要的一点是听到单词秒反应意思，但是很多时候没有合适的这样的听写音频，以测试自己的反应速度。故写此生成器。

功能：将list文件夹内的所有单词文件中的单词和词组按照数目划分成多个word list并生成音频。

## 依赖
需要的库：
pydub
tqdm
urllib

## 使用
- 使用默认设置

将你需要听写的单词的excel文件放入list文件夹中，且单词放在第一列，运行reaction_quick.py即可，生成的测试听写音频在dictate
```shell script
python reaction_quick.py
```

- 修改设置

参数说明：

type：可选'E'或'A'表示英音和美音

split：可选'random'和'order'表示打乱顺序和按照顺序

number:一个测试音频的单词或词组数

frompath： 原单词文件或文件夹

topath： 测试音频存放的文件夹

store： 存放每个单词读音的文件夹

interval_sec_in: 词组内读音的间隔，单位：s

interval_sec_out: 词组间读音的间隔，单位：s

你可以用命令行修改这些参数：
如修改为英音：
```shell script
python reaction_quick.py --type E
```

## 未完持续
- 未加入按照原划分的list生成音频的功能
- 没有增加从txt，json等文件中获取单词的功能
- 没有进行测试：包括错误单词，没有单词读音等问题
- 很多其他功能如gui和单词提醒等

## references
[1]https://github.com/zwm0426/combine-word-listening
blank文件与实例单词来自这个库

[2]下载音频来源于有道词典的API