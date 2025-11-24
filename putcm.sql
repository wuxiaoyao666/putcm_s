-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 47.93.2.246    Database: putcm
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `anquan`
--

DROP TABLE IF EXISTS `anquan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anquan` (
  `subId` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表110:安全性评价 表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anquan`
--

LOCK TABLES `anquan` WRITE;
/*!40000 ALTER TABLE `anquan` DISABLE KEYS */;
/*!40000 ALTER TABLE `anquan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bencao`
--

DROP TABLE IF EXISTS `bencao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bencao` (
  `subId` int NOT NULL AUTO_INCREMENT,
  `tcmId` int DEFAULT NULL COMMENT '中药ID',
  `t1` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药材名称',
  `tcmType` int DEFAULT NULL COMMENT '药物类型，1-植物药，2-动物药，3-矿物药，4-其他',
  `t2` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '本草记载',
  `t3` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '名称考证',
  `t4` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '基原考证',
  `t5` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药用部件考证',
  `t6` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '产地考证',
  `t7` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '性味归经考证',
  `t8` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '功能主治考证',
  `t9` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '用法用量考证',
  `t10` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '备注',
  `userId` int DEFAULT NULL COMMENT '关联表 userinfo',
  `insertTime` bigint DEFAULT NULL,
  `updateTime` bigint DEFAULT NULL,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表101:本草考证';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bencao`
--

LOCK TABLES `bencao` WRITE;
/*!40000 ALTER TABLE `bencao` DISABLE KEYS */;
INSERT INTO `bencao` VALUES (1,1,'<p><span style=\"font-family: \'Microsoft YaHei\', \'Helvetica Neue\', \'PingFang SC\', sans-serif;\">《中华人民共和国药典》（2020版）：本品为菊科植物红花<em>Carthamus tinctorius L.</em> 的干燥花。夏季花由黄变红时釆摘，阴干或晒干。功能主治：活血通经，散瘀止痛。用于经闭，痛经，恶露不行，癥瘕痞块，胸痹心痛，瘀滞腹痛，胸胁刺痛，跌扑损伤，疮疡肿痛。用法用量：3～10g。本品按干燥品计算，含山柰酚（C<sub>15</sub>H<sub>10</sub>O<sub>6</sub>）不得少于0.050%。</span></p>',1,'<p>《唐本草》：治口噤不语，血结，产后诸疾；《开宝本草》：主产后血运口噤，腹内恶血不尽、绞痛，胎死腹中，并酒煮服。亦主蛊毒下血。</p>','<p>&ldquo;红花&rdquo;一名最早出现在宋代《开宝本草》中,马志谓:&ldquo;红蓝花即红花也,生梁汉及西域。&rdquo;[6]可见在此之前,红花主要以&ldquo;红蓝花&rdquo;之名出现,而&ldquo;红蓝花&rdquo;一词的出现最早可追溯到东汉《金匮要略》的&ldquo;红蓝花酒&rdquo;。《本草图经》记载:&ldquo;其花红色,叶颇似蓝,故有蓝名。&rdquo;[7]《本草蒙筌》也记述:&ldquo;因叶似蓝,故此为誉 。&rdquo;[8]此外,在古本草中还可见红花以&ldquo;黄蓝&rdquo;之名出现,如 《证 类 本 草》之 &ldquo;生 梁、汉 及 西 域。一 名 黄蓝&rdquo;[9],《本草原始》之&ldquo;花生时,但作黄色茸茸,故一名黄蓝&hellip;&hellip;花红色,叶颇似蓝,故名红蓝花,俗呼红花&rdquo;[10]。综上,因红花原植物与&ldquo;蓝&rdquo;的叶相似,故冠以&ldquo;蓝 名&rdquo;,又 因 其 花 冠 颜 色,有 &ldquo;红 蓝 花&rdquo;&ldquo;黄 蓝&rdquo;之称。</p>','<p>《本草图经》[7]对红花原植物的描述有:&ldquo;其花红色,叶颇似蓝&rdquo;&ldquo;花下作球猬多刺,花出球上&rdquo;&ldquo;球中结实,白 棵 如 小 豆 大&rdquo;,分 别 展 现 了 其 花 冠 为 红色,叶与蓝 相 似,头 状 花 序 顶 生,总 苞 片 多 层 且 具刺,瘦果 呈 白 色 的 特 征。此 外,书 中&ldquo;人 家 场 圃 所种,冬所布子于熟地,至春生苗,夏乃有花&rdquo;的记载则对红C.tinctoriusL.生长周期进行了描绘,表明红花应于冬末(二 月)时 节 播 种 于 田 圃,春 天 发芽,夏日开花。《本草原始》[10]&ldquo;花生时,但作黄色茸茸&rdquo;的描述指出红花初开时花冠为黄色,也是红花&ldquo;黄蓝&rdquo;名称由来的一种解释。《救荒本草》载有&ldquo;苗高二尺许,茎叶有刺,似刺蓟叶而润泽&rdquo;[11],描述了红花C.tinctoriusL.成熟时株高约60cm,茎叶都有 刺,叶 形 与 大 蓟、小 蓟 相 似 而 略 光 滑 的 特征。《本草纲目》记载:&ldquo;红花叶如小蓟叶。至五月开花,如大蓟花而红色。&rdquo;[12]《增订伪药条辨》也有类似描 述:&ldquo;花 如 大 蓟,色 甚 清 红。&rdquo;[13]可 知 红 花C.tinctoriusL.叶形与小蓟相似,花形与大蓟相似<br>但为红色。综上,红花原植物与大蓟、小蓟之间存在近缘关系,历 代 本 草 关 于 红 花 原 植 物 的 描 述 与现 今 正 品 红 花 来 源 即 菊 科 红 花 属 植 物 红 花</p>','<p>有诸多文献记载了红花的形态特征。《本 草 图 经》载：&ldquo;红蓝花，生梁汉及西域，今处处有之，人家场圃所种，冬而布子于熟地，至春生苗，夏乃有花，下作球汇多刺，花蕊出球上，圃人乘露采之，采已复出，至尽而罢。球中结实，白颗如小豆大。&rdquo;贾所 学《药 品 化 义》载：&ldquo;红 花，属 阳，体 轻，色红，气膻，味辛微 苦，性 温。红 花 色 红 类 血。&rdquo;</p>','<p>关于红花原植物的起源众说纷纭。早在1926年就有学者提出红花C.tinctoriusL.的栽培有3个起源中心,分别为埃及、印度及阿富汗。1978年,日本学者星川清亲提出埃塞俄比亚是红C.tinctoriusL.的起源中心。然而,目前多数学者认为将地中海东岸的&ldquo;新月地带&rdquo;作为红花C.tinctoriusL.的起源中心较为合理。其主要证据有三:一是历史上有大量的农作物在该地区被驯化栽培并传播至世界各地;二是在该地区发现大量红花C.tinctoriusL.野生近缘种存在,且叙利亚保留有4500年前的红花C.tinctoriusL.种子;三是通过群体遗传分析找<br>到的红花C.tinctoriusL.最有可能的起源物种位于该地区[18]。</p>','<p>红花，性味归经：辛，温。归心、肝经。功效为：活血通经，祛瘀止痛。</p>','<p>《本草汇言》载：&ldquo;红花，破血行血、和血调血之药也，主胎产百病。盖血之为物，生 化于脾，总统于心，藏纳于肝，宣布于肺，施泄于肾，分属任冲，灌溉一身，红花汁与之同类，故能活男子血脉，行女人经水。红花子，治天行痘疮，血热不能起发，用数十粒，研烂，和 生犀角、真紫草、生地黄，同煎服。&rdquo;《药品化义》载：&ldquo;红 花 色红类血，味辛性温，善通利经脉，为血中气药。能泻而又 能补，各有妙义。若多用三四钱则过于辛温，使血走散。同苏木逐淤血，合肉桂 通 经 闭，佐归芎治遍身或胸腹血气刺痛，此其行异而活血也。若少用七八分，取其味辛以疏肝气，色赤以助血 海，大 补 血 虚，此 其 调 畅 而 和 血 也。若 止 用 二 三分，取其色赤入心，以配心血，又借辛味解散心经邪火，令血调 和，此其滋养而生血也。分量多寡之义岂浅 鲜 哉。&rdquo;吴谦《医宗金鉴》记载了治疗便毒的红花散瘀汤方：&ldquo;红花、当归尾、皂刺各一 钱，生 军 三 钱，连 翘（去 心）、苏 木、穿 山 甲、石决明、僵蚕（炒）、乳香、贝母各一钱，黑牵牛二钱。酒、水 各 一 钟，煎 八 分，空 心 服。行 五、六 次，方 食 稀 粥 补之。</p>','<p>《药品化义》［１４］载：&ldquo;红 花 色红类血，味辛性温，善通利经脉，为血中气药。能泻而又 能补，各有妙义。若多用三四钱则过于辛温，使血走散。同苏木逐淤血，合肉桂 通 经 闭，佐归芎治遍身或胸腹血气刺痛，此其行异而活血也。若少用七八分，取其味辛以疏肝气，色赤以助血 海，大 补 血 虚，此 其 调 畅 而 和 血 也。若 止 用 二 三分，取其色赤入心，以配心血，又借辛味解散心经邪火，令血调 和，此其滋养而生血也。分量多寡之义岂浅 鲜 哉。&rdquo;吴谦《医宗金鉴》记载了治疗便毒的红花散瘀汤方：&ldquo;红花、当归尾、皂刺各一 钱，生 军 三 钱，连 翘（去 心）、苏 木、穿 山 甲（炙研）、石决明、僵蚕（炒）、乳香、贝母各一钱，黑牵牛二钱。酒、水 各 一 钟，煎 八 分，空 心 服。行 五、六 次，方 食 稀 粥 补之。</p>','<p>对于争议问题的补充</p>',1,1762406885,1762406885);
/*!40000 ALTER TABLE `bencao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `captcha`
--

DROP TABLE IF EXISTS `captcha`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `captcha` (
  `captchaId` int NOT NULL AUTO_INCREMENT,
  `captchaText` char(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '验证码文本，4位数字',
  `genTime` bigint DEFAULT NULL COMMENT '生成时间秒数，超过5分钟则失效',
  PRIMARY KEY (`captchaId`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表002.验证码表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `captcha`
--

LOCK TABLES `captcha` WRITE;
/*!40000 ALTER TABLE `captcha` DISABLE KEYS */;
/*!40000 ALTER TABLE `captcha` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `huaxue`
--

DROP TABLE IF EXISTS `huaxue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `huaxue` (
  `subId` int NOT NULL AUTO_INCREMENT,
  `tcmId` int DEFAULT NULL COMMENT '中药ID',
  `t1` text COMMENT '药材来源',
  `t2` text COMMENT '来源部位',
  `t3` text COMMENT '药材编号',
  `t4` text COMMENT '化合物名称',
  `t5` text COMMENT '化合物描述',
  `t6` text COMMENT '英文名称',
  `t7` text COMMENT '分子式',
  `t8` text COMMENT '分子量（g/mol）',
  `t9` text COMMENT 'SMILES结构式',
  `i1` json DEFAULT NULL COMMENT '分子结构图（list，{img,title}',
  `t10` text COMMENT '理化性质',
  `t11` text COMMENT '化学结构分类',
  `t12` text COMMENT '紫外（UV）光谱',
  `t13` text COMMENT '红外（IR）光谱',
  `t14` text COMMENT '圆二色（CD）光谱',
  `t15` text COMMENT '核磁共振氢谱（1H NMR）',
  `t16` text COMMENT '核磁共振碳谱（13C NMR）',
  `t17` text COMMENT '提取方式',
  `t18` text COMMENT '含量范围（%或mg/g）',
  `t19` text COMMENT '含量变化因素',
  `t20` text COMMENT '药理活性描述',
  `t21` text COMMENT '作用靶点/通路',
  `t22` text COMMENT '文献/数据库来源',
  `t23` text COMMENT '备注说明',
  `userId` int DEFAULT NULL COMMENT '关联表 userinfo',
  `insertTime` bigint DEFAULT NULL,
  `updateTime` bigint DEFAULT NULL,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表105:化学成分';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `huaxue`
--

LOCK TABLES `huaxue` WRITE;
/*!40000 ALTER TABLE `huaxue` DISABLE KEYS */;
INSERT INTO `huaxue` VALUES (4,1,'<p>红花，本品为菊科植物红花Carthamus tinctorius L. 的干燥花。夏季花由黄变红时釆摘，阴干或晒干。</p>','<p>本品为菊科植物红花Carthamus tinctorius L. 的干燥花。</p>','<p>HYZ00001</p>','<p>羟基红花黄色素A</p>','<p>本项目新发现、已被开发利用</p>','<p>&nbsp;Hydroxysafflor yellow A</p>','<p>&nbsp; &nbsp;&nbsp;<br>C27H32O16</p>','<p>612.5 g/mol</p>','<p>C1=CC(=CC=C1/C=C/C(=C/2\\C(=C(C(=O)C(C2=O)([C@H]3[C@@H]([C@H]([C@@H]([C@H](O3)CO)O)O)O)O)[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)CO)O)O)O)O)/O)O</p>','[{\"img\": \"/api/file/1/7397537468100120576.png\", \"title\": \"分子结构式\"}]','<p>Cas号: 78281-02-4<br>沸 点: 1015.8℃&nbsp;</p>','<p>具有单查尔酮苷类结构的化合物</p>','<p>320，254 nm</p>','<p>3220, 2924, 2853, 1743, 1667, 1601, 1450, 1335, 1259, 1175, 1121, 1096, 1047, 1023, 706 cm&minus;1</p>','<p>某手性药物在 230nm 处 &Delta;&epsilon; = +2.8 M⁻&sup1;・cm⁻&sup1;，对比标准品（纯右旋体 &Delta;&epsilon; = +5.6 M⁻&sup1;・cm⁻&sup1;），可计算其 ee 值 = (2.8 / 5.6) &times; 100% = 50%（即右旋体占 75%，左旋体占 25%）。</p>','<p>化学位移数组中，&delta;=1.2 ppm、2.0 ppm、4.1 ppm 处出现 3 个信号峰（强度峰值分别为 800、1000、600）；[0.000, 0.0006, 0.0012, ..., 9.9994, 10.000]（ppm）</p>','<p>0.00, 0.0076, 0.0152, ..., 249.98, 250.00（ppm）</p>','<p>水提</p>','<p>水提含量为20&ndash;35mg/g，提取得率0.2-0.5%</p>','<p>由于品种不同含量有所差异</p>','<p>是红花药理功效的最有效水溶性部位，可抑制血小板激活因子诱发的血小板聚集与释放，可竞争性地抑制血小板激活因子与血小板受体的结合，是红花黄色素的活血化瘀有效成分。它是一种好的医药原料，也可用于制作保健和化妆品，还是很好的食品染料。抗血小板和抗心肌缺血作用。抗凝血酶诱导的血小板聚集活性，抗炎活性，细胞保护活性，抗肿瘤活性。</p>','<p>羟基红花黄色素 A（HSYA）主要通过调控多类关键信号通路发挥生物活性，在抗炎方面，可抑制 NF-&kappa;B 通路中 I&kappa;B&alpha; 的磷酸化与降解、下调 MAPK 通路中磷酸化 ERK1/2、JNK 及 p38 的表达，减少促炎细胞因子与炎症介质合成以减轻炎症；在抗氧化与细胞保护方面，能激活 Nrf2/ARE 通路，促进 Nrf2 核转位并上调 HO-1、SOD 等抗氧化酶表达，增强细胞清除 ROS 能力，保护神经细胞与心肌细胞免受氧化应激损伤，此外还可能通过调控与血栓形成、血管功能相关的通路（如影响血小板活化因子、血管内皮生长因子相关通路），发挥抗血栓、保护心血管等作用。</p>','<p>9. Wang L, Wu H-L, Yin X-L, Hu Y, Gu H-W, Yu R-Q. Simultaneous determination of umbelliferone and scopoletin in Tibetan medicine Saussurea laniceps and traditional Chinese medicine Radix angelicae pubescentis using excitation-emission matrix fluorescence coupled with second-order calibration method. Spectrochim Acta A Mol Biomol Spectrosc. 2017;170:104&ndash;10. https://doi.org/10.1016/j.saa.2016.07.018 PMID: 27423108 &nbsp;<br>10. Fang D-M, Wu H-L, Ding Y-J, Hu L-Q, Xia A-L, Yu R-Q. Interference-free determination of fluoroquinolone antibiotics in plasma by using excitation-emission matrix fluorescence coupled with second-order calibration algorithms. Talanta. 2006;70(1):58&ndash;62. https://doi.org/10.1016/j. talanta.2006.01.014 PMID: 18970729</p>','<p>用于记录异构体、立体结构、图谱连接、药代信息链接等</p>',1,1763710288,1763710400);
/*!40000 ALTER TABLE `huaxue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kaifa`
--

DROP TABLE IF EXISTS `kaifa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kaifa` (
  `subId` int NOT NULL AUTO_INCREMENT,
  `tcmId` int DEFAULT NULL COMMENT '中药ID',
  `t1` text,
  `t2` text,
  `t3` text,
  `t4` text,
  `t5` text,
  `t6` text,
  `t7` text,
  `t8` text,
  `t9` text,
  `t10` text,
  `t11` text,
  `t12` text,
  `t13` text,
  `t14` text,
  `t15` text,
  `t16` text,
  `t17` text,
  `t18` text,
  `t19` text,
  `t20` text,
  `t21` text,
  `t22` text,
  `t23` text,
  `t24` text,
  `userId` int DEFAULT NULL,
  `insertTime` bigint DEFAULT NULL,
  `updateTime` bigint DEFAULT NULL,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表112:开发利用';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kaifa`
--

LOCK TABLES `kaifa` WRITE;
/*!40000 ALTER TABLE `kaifa` DISABLE KEYS */;
INSERT INTO `kaifa` VALUES (1,1,'<p>本品为菊科植物红花Carthamus tinctorius L. 的干燥花。夏季花由黄变红时釆摘，阴干或晒干。</p>','<p>红七片</p>','<p>处方药</p>','<p>片剂</p>','<p>红花提取物30%，蔗糖、粘合剂等</p>','<p>0.5g/片</p>','<p>每日一次，一次两片</p>','<p>本品含有乳制品</p>','<p>孕期、哺乳期禁用，XXX人群禁用，患有XXX疾病禁用</p>','<p>常温、通风阴凉处保存</p>','<p>活血化瘀</p>','<p>医院临床人群</p>','<p>已批准上市</p>','<p>国药准字Z20012345</p>','<p>北京大学天然药物实验室</p>','<p>生产可能先对红花药材进行筛选，确保药材的质量和纯度。然后进行粉碎，将红花粉碎成细粉，过一定目数的筛网，如 80 目或 100 目筛。之后可能加入适量的辅料，如淀粉、预胶化淀粉等，与红花粉混合均匀，再通过湿法制粒等方法制成颗粒，颗粒经干燥、整粒后，加入硬脂酸镁等润滑剂混合均匀，最后进行压片操作，制成红七片。压片过程中需控制片重差异、硬度、外观等质量指标。压片完成后，进行包装，包括内包装和外包装，内包装如铝塑包装，外包装如装盒、装箱等。</p>','<p>得率为8.3%</p>','<p>发明专利号：CN123456789A</p>','<p>参考资料为产品说明书</p>','<p>提取物精制后药渣用于饲料、</p>','<p>主要销售于中国及东南亚等地区</p>','<p>年产量为100万盒</p>','<p>暂无公开的用户满意度统计信息</p>','<p>从成本导向来看，需精准核算全产业链成本构成，核心包括原料成本（红花药材的采购价，受产地、品相、炮制工艺影响，如道地红花单价高于普通红花，醋制、酒制等炮制加工会增加成本；若红七片含其他配伍药材，需叠加对应原料成本）、生产加工成本（药材提取、制粒、压片、包衣等工艺费用，以及辅料、能耗、设备折旧）、合规成本（药品 / 保健品的研发、临床验证、审批备案费用，中药制剂还需包含质量检测如有效成分含量测定等费用）及运营成本（包装、仓储、物流、营销推广等），在此基础上叠加合理利润（通常药品利润空间受政策调控，保健品利润相对灵活），形成基础定价底线。</p>',1,1763968264,1763968264);
/*!40000 ALTER TABLE `kaifa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `linchuang`
--

DROP TABLE IF EXISTS `linchuang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `linchuang` (
  `subId` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表111:临床应用';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `linchuang`
--

LOCK TABLES `linchuang` WRITE;
/*!40000 ALTER TABLE `linchuang` DISABLE KEYS */;
/*!40000 ALTER TABLE `linchuang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tcm`
--

DROP TABLE IF EXISTS `tcm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tcm` (
  `tcmId` int NOT NULL,
  `tcmName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `letterIndex` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '首字母索引',
  `allLetter` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '全拼，用于同字母下排序',
  `tcmImg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '图片完整路径，从/tcm开始，含后缀',
  `insertUserId` int DEFAULT NULL,
  `insertTime` bigint DEFAULT NULL,
  `updateTime` bigint DEFAULT NULL,
  PRIMARY KEY (`tcmId` DESC) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表003:中药名表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tcm`
--

LOCK TABLES `tcm` WRITE;
/*!40000 ALTER TABLE `tcm` DISABLE KEYS */;
INSERT INTO `tcm` VALUES (2,'黄芪','H','huangqi','/api/file/tcm/7391367557304815616.jpg',1,1762239351,1762239351),(1,'红花','H','honghua','/api/file/tcm/7391367362588446720.jpg',1,1762239307,1762239307);
/*!40000 ALTER TABLE `tcm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tiqu`
--

DROP TABLE IF EXISTS `tiqu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tiqu` (
  `subId` int NOT NULL AUTO_INCREMENT,
  `tcmId` int DEFAULT NULL COMMENT '中药ID',
  `t1` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药材基源',
  `t2` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '原植物',
  `t3` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '提取部位',
  `t4` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '预处理方法',
  `t5` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '提取方式',
  `t6` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '提取参数',
  `t7` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '提取设备型号',
  `t8` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '过滤方式',
  `t9` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '过滤参数',
  `t10` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '分离方式',
  `t11` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '分离参数',
  `t12` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '浓缩方式',
  `t13` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '浓缩参数',
  `t14` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '干燥方式',
  `t15` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '干燥参数',
  `t16` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '最终产物形态',
  `t17` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '得率（%）',
  `t18` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '工艺规模',
  `t19` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '目标成分名称',
  `t20` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '目标成分要求',
  `t21` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '目标成分检测方法依据',
  `i1` json DEFAULT NULL COMMENT '相关图谱（list，{img,title}',
  `t22` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '工艺来源',
  `t23` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '引用文献/说明书',
  `t24` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '备注说明',
  `userId` int DEFAULT NULL COMMENT '关联表 userinfo',
  `insertTime` bigint DEFAULT NULL,
  `updateTime` bigint DEFAULT NULL,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表104:提取分离';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tiqu`
--

LOCK TABLES `tiqu` WRITE;
/*!40000 ALTER TABLE `tiqu` DISABLE KEYS */;
INSERT INTO `tiqu` VALUES (1,1,'<p>红花，本品为菊科植物红花<em>Carthamus tinctorius L.</em> 的干燥花。夏季花由黄变红时釆摘，阴干或晒干。1</p>','<p>菊科植物红花（Carthamus tinctorius L.）</p>','<p>菊科植物红花Carthamus tinctorius L.的花</p>','<p>红花提取前的预处理需先筛选出干燥、无霉变虫蛀的药材，去除花萼、花梗、泥沙等杂质，用去离子水快速冲洗以避免活性成分流失，随后置于 40~50℃烘箱低温烘干（防止羟基红花黄色素 A 等热敏性成分降解），并粉碎至 20~40 目（颗粒过细易结块堵塞、过粗则提取不充分）；若目标成分为极性较低的脂肪酸，可额外用 60~90℃石油醚回流提取 1~2 次（每次 2h）进行脱脂处理，弃去石油醚相后晾干残渣；若需提升黄酮类成分溶出效率，还可对粉碎后的红花进行 300W 功率、15min 时长的超声预处理，借助超声空化效应破坏细胞壁结构，为后续提取工序奠定基础。</p>','<p>超声提取红花时，先取经预处理（筛选去杂、40~50℃烘干、粉碎至 20~40 目，若需脱脂则已用 60~90℃石油醚回流处理）的红花粉末，按 1:10~1:15 的料液比加入 70% 乙醇（针对黄酮类等中等极性活性成分），置于超声提取设备中，设定功率 300~500W、提取温度 50~60℃（低温保护羟基红花黄色素 A 等热敏成分），持续超声处理 40~60min，期间借助超声空化效应加速活性成分溶出，提取结束后过滤分离，收集滤液即得红花超声提取液，后续可根据需求进行纯化处理。</p>','<p>用超声辅助提取（适用于黄酮类等成分），则以 70%~80% 乙醇（或去离子水，针对水溶性成分）为溶剂，按 1:10~1:15 的料液比混合预处理后的红花粉末，设定 300~500W 超声功率、20~40kHz 超声频率、50~60℃提取温度，持续提取 40~60min；若选择乙醇回流提取，同样用 70%~80% 乙醇，料液比 1:10~1:20，在 70~75℃下保持微沸状态回流 2 次，每次 1.5~2h；若为热水提取（针对水溶性成分），则以去离子水为溶剂，料液比 1:15~1:25，在 80~90℃下提取 2~3 次，每次 1.5h，期间可配合 100~200r/min 搅拌速率提升溶出效率。</p>','<p>红花提取过程中，原料预处理阶段需用中药材粉碎机（将烘干红花粉碎至 20-40 目）、标准检验筛（筛选对应目数粉末）和鼓风干燥箱（40-50℃烘干清洗后药材）；核心提取阶段，超声辅助提取用带控温夹套（50-60℃）、功率 100-600W、频率 20-40kHz 的超声提取仪，乙醇回流提取用带加热装置（控温 70-75℃）、冷凝管的回流提取装置（实验室用圆底烧瓶搭配，工业化用多联式回流提取罐），热水提取用可控温 80-90℃的恒温水浴锅（实验室）或热水提取罐（工业化）；提取后还需布氏漏斗与抽滤瓶（实验室快速抽滤）、板框压滤机（工业化固液分离），以及旋转蒸发仪（实验室回收乙醇）、乙醇回收塔（工业化溶剂回收）等仪器配合完成流程。</p>','<p>红花提取液进行板框过滤时，先将经超声、回流或热水提取后得到的粗提取液（含红花残渣颗粒、少量多糖等杂质）预热至 30~40℃（降低液体黏度，提升过滤效率），随后启动板框压滤机，将提取液通过进料泵以 0.2~0.4MPa 的压力注入由滤板、滤框交替组成的过滤腔室，借助滤布（常用涤纶或丙纶材质，孔径 5~10&mu;m，可截留粒径大于滤布孔径的残渣与大颗粒杂质）实现固液分离，过滤过程中需控制进料速率均匀（避免压力骤升导致滤布破损），待滤板表面形成一定厚度的滤饼（可减少后续杂质穿透）后，持续收集从滤板出液口流出的澄清红花提取液，过滤结束后停机拆卸板框，清理滤饼（可用于后续残渣再提取或无害化处理）并清洗滤布，以备下次使用，最终得到的澄清提取液可进入后续纯化（如大孔树脂吸附）或浓缩工序。</p>','<p>红花提取液板框过滤的关键参数需围绕效率与澄清度设定，进料压力控制在 0.2~0.4MPa（压力过低则过滤速度慢，过高易致滤布破损、杂质穿透），提取液需预热至 30~40℃（降低液体黏度以提升过滤效率，避免低温下多糖等成分析出堵塞滤布），选用孔径 5~10&mu;m 的涤纶或丙纶滤布（截留提取液中残渣颗粒与大尺寸杂质，同时保证有效成分顺利通过），进料速率需保持均匀稳定（通常根据设备规格控制在 1~3m&sup3;/h，防止局部压力骤升影响过滤效果），滤饼厚度控制在 5~10mm（过薄则滤布利用率低，过厚易导致过滤阻力增大、速率下降），确保最终得到澄清无明显残渣的提取液，满足后续纯化或浓缩工序要求。</p>','<p>先对板框过滤后的澄清提取液进行初步分离，若目标成分为水溶性成分（如羟基红花黄色素 A），可通过减压浓缩（温度 50~60℃、真空度 0.06~0.08MPa）去除部分溶剂，减少后续处理量；若含醇溶性杂质，可加入适量去离子水稀释（降低醇浓度至 30% 以下），促使多糖、蛋白质等杂质析出，再经离心（转速 3000~5000r/min，时间 10~15min）或微滤（膜孔径 0.22~0.45&mu;m）进一步除杂。<br>随后进入精制分离阶段，主流采用大孔树脂吸附法：将预处理后的提取液调节 pH 至 5~6（匹配树脂吸附条件），以 2~4BV/h（床体积 / 小时）的流速通过 AB-8 或 D101 型大孔树脂柱，让目标成分充分吸附；接着用 30% 乙醇以 1~2BV/h 流速洗脱（去除弱吸附杂质），再用 70%~80% 乙醇以 2~3BV/h 流速洗脱目标成分，收集洗脱液；若需更高纯度，可对洗脱液进行聚酰胺柱层析（洗脱剂用 50%~60% 乙醇）或高速逆流色谱（溶剂体系如正丁醇 - 乙酸 - 水 = 4:1:5），最终通过减压浓缩、冷冻干燥（温度 - 40~-50℃，真空度 0.09~0.1MPa）得到高纯度红花活性成分粉末，完成分离全过程。</p>','<p>红花提取液分离过程中，各环节关键参数需精准控制以保障除杂效果与目标成分回收率，具体参数如下：初步分离阶段，减压浓缩需设定温度 50~60℃、真空度 0.06~0.08MPa（低温避免热敏成分降解，适宜真空度加速溶剂挥发）；若需稀释除杂，乙醇浓度需降至 30% 以下，后续离心参数为转速 3000~5000r/min、时间 10~15min（确保多糖、蛋白质等杂质充分沉降），微滤则选用 0.22~0.45&mu;m 孔径的微滤膜。精制分离阶段，大孔树脂吸附前需将提取液 pH 调至 5~6，上柱流速控制为 2~4BV/h（BV 为树脂床体积，保证目标成分充分吸附）；洗脱时先用 30% 乙醇以 1~2BV/h 流速洗脱杂质，再用 70%~80% 乙醇以 2~3BV/h 流速洗脱目标成分；若采用聚酰胺柱层析，洗脱剂为 50%~60% 乙醇；高速逆流色谱则选用正丁醇 - 乙酸 - 水 = 4:1:5 的溶剂体系。最终产物制备阶段，冷冻干燥参数为温度 - 40~-50℃、真空度 0.09~0.1MPa（保障活性成分稳定，形成疏松粉末）。</p>','<p>先将前期经大孔树脂洗脱或微滤后的分离液（乙醇浓度多为 30%~80%，含目标黄酮类成分）预热至 40~50℃（降低黏度，便于成膜），随后通过进料泵以 1~2BV/h（针对树脂洗脱液）的流速，均匀输送至薄膜蒸发器（常用升膜式或降膜式，实验室用小型旋转薄膜蒸发器，工业化用多效降膜蒸发器）的加热管内；浓缩过程中，加热介质（如热水或低压蒸汽）温度控制在 60~70℃，蒸发器内维持 0.07~0.09MPa 的高真空度（降低溶剂沸点，避免高温破坏活性成分），分离液在加热管内壁形成 0.1~0.5mm 的薄液膜，受重力或离心力作用向下流动，同时与加热面充分接触，溶剂（乙醇或水）快速汽化并进入冷凝系统，冷凝后回收再利用；浓缩后的物料（即浓缩液）从蒸发器底部出料口收集，需控制其固形物含量达到 15%~25%（根据后续干燥需求调整，固形物过低会增加干燥能耗，过高易导致管路堵塞），期间需实时监测出料温度（稳定在 55~65℃）与固形物含量，确保浓缩效果稳定；若需进一步提高浓度，可将初次浓缩液再次泵入蒸发器进行二次浓缩，最终得到的浓缩液可直接用于冷冻干燥或喷雾干燥，制备高纯度红花活性成分粉末。</p>','<p>先将分离液预热至 40~50℃（降低黏度以利成膜），以 1~2BV/h 的流速（针对树脂洗脱液）输送至薄膜蒸发器；加热介质（热水 / 低压蒸汽）温度控制在 60~70℃，蒸发器内维持 0.07~0.09MPa 高真空度（降低溶剂沸点，避免高温破坏羟基红花黄色素 A 等热敏成分），确保分离液在加热管内壁形成 0.1~0.5mm 薄液膜；浓缩后需控制出料固形物含量为 15%~25%（适配后续干燥需求，过低增加干燥能耗、过高易堵管路），出料温度稳定在 55~65℃，若需进一步浓缩可进行二次处理，期间实时监测固形物含量与温度，保障浓缩效果与成分稳定性。</p>','<p>先将薄膜浓缩后固形物含量 15%~25% 的浓缩液（若黏度偏高，可加少量去离子水调节至黏度 50~100mPa・s，避免堵塞雾化器）预热至 50~60℃，通过进料泵以 8~15mL/min（实验室小型喷雾干燥机）或按设备产能匹配的流速（工业化设备按每小时处理量调整），输送至喷雾干燥机的离心式或压力式雾化器；干燥过程中，控制进风温度 160~180℃（高温快速雾化液滴，缩短受热时间）、出风温度 70~80℃（温度过低易导致粉末黏壁，过高会破坏活性成分），干燥塔内维持微负压（-5~-10kPa，利于湿气排出与粉末收集）；雾化器转速（离心式）控制在 20000~30000r/min（或压力式雾化器压力 0.2~0.4MPa），确保浓缩液雾化成直径 5~20&mu;m 的细小液滴，与热空气充分接触，瞬间完成水分 / 溶剂蒸发；干燥后的粉末经旋风分离器（分离效率&ge;95%）收集，若需提升纯度，可配合布袋除尘器进一步捕集细粉；最终得到的红花活性成分粉末含水量需控制在 3%~5%（保障储存稳定性，避免吸潮结块），该干燥方式适配工业化连续生产，且粉末流动性好、溶解性佳，便于后续制剂加工（如片剂、胶囊剂）或直接应用。</p>','<p>红花提取浓缩液喷雾干燥的关键参数需兼顾干燥效率与成分稳定性，具体如下：将固形物含量 15%~25% 的浓缩液（黏度调至 50~100mPa・s）预热至 50~60℃，以 8~15mL/min（实验室）或匹配设备产能的流速进料；采用离心式雾化器时转速 20000~30000r/min（压力式则控制压力 0.2~0.4MPa），确保雾化成 5~20&mu;m 液滴；进风温度 160~180℃（快速蒸发水分），出风温度 70~80℃（避免成分降解与黏壁）；干燥塔内维持 - 5~-10kPa 微负压（利于排湿与收集）；最终粉末含水量控制在 3%~5%，经旋风分离器（分离效率&ge;95%）收集，保障产物流动性好、溶解性佳且活性成分稳定。</p>','<p>干浸膏粉等</p>','<p>提取分离的最终得率为36%</p>','<p>中试，规模为1-50kg</p>','<p>目标成分羟基红花黄色素A</p>','<p>羟基红花黄色素A&ge;2%</p>','<p>《中国药典》：羟基红花黄色素A &nbsp;照高效液相色谱法（通则0512）测定。<br>　　色谱条件与系统适用性试验 &nbsp;以十八烷基硅烷键合硅胶为填充剂；以甲醇-乙腈-0.7%磷酸溶液（26：2：72）为流动相；检测波长为403nm。理论板数按羟基红花黄色素A峰计算应不低于3000。<br>　　对照品溶液的制备 &nbsp;取羟基红花黄色素A对照品适量，精密称定，加25%甲醇制成每1ml含0.13mg的溶液，即得。<br>　　供试品溶液的制备 &nbsp;取本品粉末（过三号筛）约0.4g，精密称定，置具塞锥形瓶中，精密加入25%甲醇50ml，称定重量，超声处理（功率300W，频率50kHz）40分钟，放冷，再称定重量，用25%甲醇补足减失的重量，摇匀，滤过，取续滤液，即得。<br>　　测定法 &nbsp;分别精密吸取对照品溶液与供试品溶液各10&mu;l，注入液相色谱仪，测定，即得。<br>　　本品按干燥品计算，含羟基红花黄色素A（C27H32O16）不得少于1.0%。</p>','[{\"img\": \"/api/file/1/7395376801737871360.png\", \"title\": \"测试1\"}]','<p>《中国药典》</p>','<p>说明书：本红花活性成分（黄酮类）提取分离工艺，以制备纯度&ge;80%、含水量 3%~5% 的提取物粉末为目标，选用含水量&le;12%、杂质&le;3% 的红花药材，经振动筛去杂、去离子水速洗、40~50℃鼓风烘干（至含水量&le;8%）、10000~12000r/min 粉碎并筛选 20~40 目粉末后，按 1:12 料液比加 70% 乙醇，在 300~400W 功率、25~30kHz 频率、55~60℃下超声提取 50~60min（至羟基红花黄色素 A 含量差值&le;2%）；提取液预热至 35~40℃，以 0.25~0.35MPa 压力、1.5~2m&sup3;/h 流速经 400mm&times;400mm 板框压滤机（5~10&mu;m 涤纶滤布）过滤，收集透光率&ge;90% 的滤液；滤液在 55~60℃、0.07~0.08MPa 下减压浓缩至 1/5~1/6 体积（乙醇回收率&ge;90%），加 3 倍去离子水稀释静置 2h 后，以 4000~4500r/min 离心 12~15min 取上清；上清液调 pH 至 5.5~6.0，以 3BV/h 流速过预处理后的 AB-8 型大孔树脂柱（静置 1h 吸附），先 30% 乙醇 1~2BV/h 洗脱杂质，再 70%~80% 乙醇 2~3BV/h 洗脱目标成分；洗脱液在 40~50℃预热、1~2BV/h 流速下，于 60~70℃加热、0.07~0.09MPa 真空的薄膜蒸发器中浓缩至固形物 15%~25%（出料温度 55~65℃）；最后将浓缩液（调黏度 50~100mPa・s、50~60℃预热）以 8~15mL/min 流速（实验室）送入喷雾干燥机，在 20000~30000r/min 离心雾化（或 0.2~0.4MPa 压力雾化）、160~180℃进风、70~80℃出风、-5~-10kPa 微负压条件下干燥，收集含水量 3%~5% 的粉末，经检验合格后包装储存。</p>','<p>工艺特殊注意事项、设备替代方案、相关优化建议等</p>',1,1763192672,1763195238);
/*!40000 ALTER TABLE `tiqu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tmpfile`
--

DROP TABLE IF EXISTS `tmpfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tmpfile` (
  `tmpFileId` int NOT NULL AUTO_INCREMENT,
  `tmpFilePath` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '从/开始，不含根目录file',
  `fileDesc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '文件描述，如：上传页面等',
  `insertTime` bigint DEFAULT NULL COMMENT '上传时间',
  PRIMARY KEY (`tmpFileId` DESC) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表004:临时添加文件表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tmpfile`
--

LOCK TABLES `tmpfile` WRITE;
/*!40000 ALTER TABLE `tmpfile` DISABLE KEYS */;
/*!40000 ALTER TABLE `tmpfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userinfo`
--

DROP TABLE IF EXISTS `userinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userinfo` (
  `userId` int NOT NULL AUTO_INCREMENT,
  `userName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `userRole` int NOT NULL COMMENT '1-管理员，2-普通用户',
  `recentlyView` json DEFAULT NULL COMMENT '中药ID数组',
  `insertTime` bigint DEFAULT NULL,
  `updateTime` bigint DEFAULT NULL,
  `lastLoginTime` bigint DEFAULT NULL,
  `authToken` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`userId`,`userRole`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表001.用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userinfo`
--

LOCK TABLES `userinfo` WRITE;
/*!40000 ALTER TABLE `userinfo` DISABLE KEYS */;
INSERT INTO `userinfo` VALUES (1,'admin','admin',1,'[1, 2, 3]',0,0,1763968434,'7398619856888664064');
/*!40000 ALTER TABLE `userinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wenxian`
--

DROP TABLE IF EXISTS `wenxian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wenxian` (
  `subId` int NOT NULL AUTO_INCREMENT,
  `tcmId` int DEFAULT NULL,
  `t1` text,
  `t2` text,
  `t3` text,
  `t4` text,
  `t5` text,
  `t6` text,
  `t7` text,
  `t8` text,
  `t9` text,
  `t10` text,
  `t11` text,
  `t12` text,
  `t13` text,
  `userId` int DEFAULT NULL,
  `insertTime` bigint DEFAULT NULL,
  `updateTime` bigint DEFAULT NULL,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表113:文献数据';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wenxian`
--

LOCK TABLES `wenxian` WRITE;
/*!40000 ALTER TABLE `wenxian` DISABLE KEYS */;
INSERT INTO `wenxian` VALUES (1,1,'<p>本品为菊科植物红花Carthamus tinctorius L. 的干燥花。夏季花由黄变红时釆摘，阴干或晒干。</p>','<p>《红花的本草考证》</p>','<p>期刊论文</p>','<p>梁从莲、陈文彬、杨然、刘谦、刘红燕</p>','<p>安徽中医药大学学报</p>','2027','<p>&nbsp;.2024 ,43 (03)&nbsp;</p>','<p>DOI:10.1016/j.jep.2022.114632</p>','<p>中文</p>','<p>红花;名称;来源;产地;用途;采收炮制;考证;</p>','<p>以历代中医药古籍中相关记载为依据，对红花名称、来源、产地、用途、采收炮制等内容进行系统考证，以期为红花资源的开发利用提供参考。红花以&ldquo;红蓝花&rdquo;之名首载于《金匮要略》,红花一名首见于《开宝本草》,历史上红花还有&ldquo;黄蓝&rdquo;之称。红花主流品种为菊科红花属植物红花Carthamus tinctorius L.,其栽培历史悠久，种植范围广泛，目前中国的主要产区有新疆、四川、云南等地。红花的花在中国古代主要用作染料，或入药用于治疗妇科疾病，红花的苗、种子或加工成的胭脂在历史上也曾有药用记载。历史上酒制红花曾为主流炮制方法，现在红花多以生品入药。</p>','<p>基源考证</p>','<p>本文献有部分争议信息需要纠正</p>',1,1763708976,1763711224);
/*!40000 ALTER TABLE `wenxian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `yaoli`
--

DROP TABLE IF EXISTS `yaoli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `yaoli` (
  `subId` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表108:药理作用';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `yaoli`
--

LOCK TABLES `yaoli` WRITE;
/*!40000 ALTER TABLE `yaoli` DISABLE KEYS */;
/*!40000 ALTER TABLE `yaoli` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `yaowu`
--

DROP TABLE IF EXISTS `yaowu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `yaowu` (
  `subId` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表109:药物代谢与药代动力学';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `yaowu`
--

LOCK TABLES `yaowu` WRITE;
/*!40000 ALTER TABLE `yaowu` DISABLE KEYS */;
/*!40000 ALTER TABLE `yaowu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `yinpian`
--

DROP TABLE IF EXISTS `yinpian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `yinpian` (
  `subId` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表107:饮片炮制';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `yinpian`
--

LOCK TABLES `yinpian` WRITE;
/*!40000 ALTER TABLE `yinpian` DISABLE KEYS */;
/*!40000 ALTER TABLE `yinpian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zaipei`
--

DROP TABLE IF EXISTS `zaipei`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zaipei` (
  `subId` int NOT NULL AUTO_INCREMENT,
  `tcmId` int DEFAULT NULL COMMENT '中药ID',
  `t1` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药材名称',
  `t2` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '基原及种质',
  `t3` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '选育品种名称',
  `t4` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '繁育方式',
  `t5` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '播种方式',
  `t6` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '繁殖方式',
  `t7` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '播种或移栽、定植时间',
  `t8` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '田间管理措施',
  `t9` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '大气要求',
  `t10` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '土壤要求',
  `t11` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '肥料使用',
  `t12` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '病虫害防治措施',
  `t13` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '最佳采收期',
  `t14` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '产地加工',
  `t15` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '产量范围',
  `t16` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '适宜生境',
  `t17` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '技术来源',
  `t18` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '参考文献/标准',
  `t19` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '备注',
  `userId` int DEFAULT NULL COMMENT '关联表 userinfo',
  `insertTime` bigint DEFAULT NULL,
  `updateTime` bigint DEFAULT NULL,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表103:栽培（养殖）技术';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zaipei`
--

LOCK TABLES `zaipei` WRITE;
/*!40000 ALTER TABLE `zaipei` DISABLE KEYS */;
INSERT INTO `zaipei` VALUES (1,1,'<p>红花，本品为菊科植物红花<em>Carthamus tinctorius L.</em> 的干燥花。夏季花由黄变红时釆摘，阴干或晒干。1</p>','<p>(1)大红花：此品种刺较少，叶子尖，花淡红色，花朵小而花丝较短，花的品质较硬。<br>(2)金红花：刺少、叶子尖端圆，花苞金红，花朵较大，花丝长，花的品质柔软。<br>(3)新疆红花：叶缘和总苞片均无刺(但也有一种有刺的)，品质较好。这种品种无刺有利于采收。</p>','<p>膜荚黄芪内蒙一号、红花&ldquo;金红1号等</p>','<p>常规选育、杂交育种、组织培养、转基号等</p>','<p>撒播</p>','<p>选择发育良好、分蘖多、花朵大而色泽好的植株作为种株。采种要采中心花蕾的籽，侧枝上的花籽不宜选作种用。俟红花茎叶呈黄棕色时种籽即成熟。以后分收分打，每667平方米可收种子50～75千克。把收下来的种籽，用簸箕簸出劣籽，储藏于瓦坛或不易受潮的器皿内，以备播种用。储藏期以不超过1年为好，否则发芽率差，长不好。</p>','<p>红花可根据地区气候，采取春播、秋播、冬播。江浙多系霜降后至立冬时播种;河南、山东多是秋播，新疆和东北寒冷地区多是春播。冬播最迟不得迟于11月底，过迟则翌年幼苗细少幼嫩，易受害虫侵袭。而四川则多为霜降前10月中旬播种。</p>','<p>间苗追肥：苗长至7厘米左右时进行间苗，选苗叶色青绿、茎粗壮的，拔去色黄而幼弱的苗，每穴留苗两三株，如有缺苗，此时可进行补填。叶苗长有5片时，用人粪尿150～250千克，每100千克对清水250千克，进行第1次追肥，追肥时从旁边浇下，防止倒伏。在惊蛰前后进行第2次追肥，每667平方米施用人粪尿500～600千克，用清水稀释。施后结合培土，以防花蕾过多倒伏。以后看生长情况，一般不再施肥。如天气久旱不雨，可适当进行灌溉。</p>','<p>红花比较喜欢温暖干燥的生长环境，耐寒性比较强，而且也耐涝，在进行种植的时候，需要使用排水性良好、比较肥沃的砂土，在平时要有充足的阳光照射，可以让其有良好的长势，还要有适宜的温度环境。 红花比较喜欢温暖的生长气候，在进行生长的时候，需要将温度保持在20-25度之间，温度不可以太低，不然会影响生长发育。</p>','<p>红花是一种喜欢干旱和较肥沃土壤的植物，也能适应瘠薄土质。潮湿与积水地对它生长不利。故应选用旱地或生荒土种植，并可在屋前后的小园地、坟堆等含有多量腐殖质的地上，适宜沙质壤土或轻度的黏土。忌连作，须隔3～4年方可种植。前作物以黄麻、大豆、冬瓜、芋头等为宜。前作物收获后，用锄头和四齿耙翻土1～2次，精耕细耙，使土壤疏松细匀，排水良好;翻土20～23厘米深，并于翻土时同时施入腐熟后的堆肥或厩肥1000千克，加过磷酸钙15千克。</p>','<p>间苗追肥：苗长至7厘米左右时进行间苗，选苗叶色青绿、茎粗壮的，拔去色黄而幼弱的苗，每穴留苗两三株，如有缺苗，此时可进行补填。叶苗长有5片时，用人粪尿150～250千克，每100千克对清水250千克，进行第1次追肥，追肥时从旁边浇下，防止倒伏。在惊蛰前后进行第2次追肥，每667平方米施用人粪尿500～600千克，用清水稀释。施后结合培土，以防花蕾过多倒伏。以后看生长情况，一般不再施肥。如天气久旱不雨，可适当进行灌溉。</p>','<p>根腐病：由根腐病菌浸染，整个生长阶段均可能发生，尤其在幼苗期、开花期发病严重。发病后植物萎缩，呈浅黄色，最后死亡。防治方法：实行轮作，选用无病地的植株留种;拔除病株，清除残枝病叶，集中烧毁。用50%退菌特500倍液加5%石灰和0.2%尿素淋喷。</p>','<p>立夏后开始采收，采收期15～20天。花瓣初开时为黄色，渐呈橙红色，最后成暗红色，当花呈橙红色时是采收最适宜的时候。每个花序可以采摘3次。由于红花药用部分是花冠，如不及时采摘，容易凋萎，故必须每天采收1次，一般多于清晨露水未干前进行，因红花锐刺甚多，日出后刺硬伤人。采收时用拇指、食指、中指捏紧，抽出花冠，太小的待翌晨采。如天气由晴转阴雨时，要组织力量抢收。</p>','<p>采收后，即行暴晒，晒时每隔半小时或1小时须用竹筷轻翻，晒半天后，再用白纸盖着晒，必须勤翻动，以保持它的色泽。如遇雨天可用无烟炭火炕干，火力要温和均匀。晴天采收的约4千克湿红花可得干红花1千克。</p>','<p>每667平方米可收干红花10～15千克，高的可达15～25千克。</p>','<p>红花适应性较强，具有喜光、耐旱、耐寒、耐盐碱、怕涝、怕高温，忌湿的特性。多栽培于气候温和、阳光充足，地势高燥，肥力中等，排水良好的而质地疏松的沙质壤土。</p>','<p>企业实践等</p>','<p>《中药材标准化栽培技术》、《绿色防控实用手册》等</p>','<p>包括特殊气候应对方式、绿色有机种植附加条件等</p>',1,1763179788,1763180478);
/*!40000 ALTER TABLE `zaipei` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zhiliang`
--

DROP TABLE IF EXISTS `zhiliang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zhiliang` (
  `subId` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表106:质量分析';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zhiliang`
--

LOCK TABLES `zhiliang` WRITE;
/*!40000 ALTER TABLE `zhiliang` DISABLE KEYS */;
/*!40000 ALTER TABLE `zhiliang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zhiwu`
--

DROP TABLE IF EXISTS `zhiwu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zhiwu` (
  `subId` int NOT NULL AUTO_INCREMENT,
  `tcmId` int DEFAULT NULL COMMENT '中药ID',
  `t1` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '药材基源',
  `t2` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '形态描述',
  `i1` json DEFAULT NULL COMMENT '形态图片（list，{img,title}',
  `t3` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '自然分布区',
  `t4` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '养殖种植区域',
  `t5` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '来源典籍文献',
  `t6` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '备注',
  `userId` int DEFAULT NULL COMMENT '关联表 userinfo',
  `insertTime` bigint DEFAULT NULL,
  `updateTime` bigint DEFAULT NULL,
  PRIMARY KEY (`subId`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='表102:原植物（动物）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zhiwu`
--

LOCK TABLES `zhiwu` WRITE;
/*!40000 ALTER TABLE `zhiwu` DISABLE KEYS */;
INSERT INTO `zhiwu` VALUES (1,1,'<p>红花，本品为菊科植物红花<em>Carthamus tinctorius L.</em> 的干燥花。夏季花由黄变红时釆摘，阴干或晒干。1</p>','<p>菊科植物红花（Carthamus tinctorius L.）</p>','null','<p>菊科植物红花Carthamus tinctorius L.的花</p>','<p>红花提取前的预处理需先筛选出干燥、无霉变虫蛀的药材，去除花萼、花梗、泥沙等杂质，用去离子水快速冲洗以避免活性成分流失，随后置于 40~50℃烘箱低温烘干（防止羟基红花黄色素 A 等热敏性成分降解），并粉碎至 20~40 目（颗粒过细易结块堵塞、过粗则提取不充分）；若目标成分为极性较低的脂肪酸，可额外用 60~90℃石油醚回流提取 1~2 次（每次 2h）进行脱脂处理，弃去石油醚相后晾干残渣；若需提升黄酮类成分溶出效率，还可对粉碎后的红花进行 300W 功率、15min 时长的超声预处理，借助超声空化效应破坏细胞壁结构，为后续提取工序奠定基础。</p>','<p>超声提取红花时，先取经预处理（筛选去杂、40~50℃烘干、粉碎至 20~40 目，若需脱脂则已用 60~90℃石油醚回流处理）的红花粉末，按 1:10~1:15 的料液比加入 70% 乙醇（针对黄酮类等中等极性活性成分），置于超声提取设备中，设定功率 300~500W、提取温度 50~60℃（低温保护羟基红花黄色素 A 等热敏成分），持续超声处理 40~60min，期间借助超声空化效应加速活性成分溶出，提取结束后过滤分离，收集滤液即得红花超声提取液，后续可根据需求进行纯化处理。</p>','<p>用超声辅助提取（适用于黄酮类等成分），则以 70%~80% 乙醇（或去离子水，针对水溶性成分）为溶剂，按 1:10~1:15 的料液比混合预处理后的红花粉末，设定 300~500W 超声功率、20~40kHz 超声频率、50~60℃提取温度，持续提取 40~60min；若选择乙醇回流提取，同样用 70%~80% 乙醇，料液比 1:10~1:20，在 70~75℃下保持微沸状态回流 2 次，每次 1.5~2h；若为热水提取（针对水溶性成分），则以去离子水为溶剂，料液比 1:15~1:25，在 80~90℃下提取 2~3 次，每次 1.5h，期间可配合 100~200r/min 搅拌速率提升溶出效率。</p>',1,1762745051,1763192867);
/*!40000 ALTER TABLE `zhiwu` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-24 15:18:10
