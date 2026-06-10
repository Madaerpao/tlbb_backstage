-- ==============================================================================
-- 脚本名称: XYNS_SecondsTimer.lua
-- 功能描述: 服务端秒级心跳定时器，用于定时轮询 Web 接口并执行 GM 指令
-- 实现方法: 
--   1. 通过 wget 命令请求 Web 后台的 API 获取未执行的指令。
--   2. 将指令解析后，根据事件类型 (Event) 分发到对应的功能函数中。
--   3. 执行完成后，将日志记录到本地文件中。
-- ==============================================================================

-- 脚本全局唯一标识符
x666898_g_scriptId = 666898

-- ==============================================================================
-- 函数名称: x666898_OnCharacterTimer
-- 功能描述: 心跳触发入口函数，由绑定了该脚本的 NPC 每秒（或固定间隔）触发
-- 参数列表:
--   sceneId - 当前场景的 ID
--   objId   - 触发该事件的对象 ID（如 NPC 的 ObjId）
--   dataId  - 数据 ID
--   uTime   - 当前的时间戳或触发次数
-- ==============================================================================
function x666898_OnCharacterTimer( sceneId, objId, dataId, uTime )
	-- 检查全局变量 GMDATA_ISOPEN_GMTOOLS 是否在 ScriptGlobal.lua 中被设置为 1 (开启)
	if GMDATA_ISOPEN_GMTOOLS == 1 then
		
		-- 1. 通过系统命令行 (execute) 调用 wget，从 Web 后台 API 获取事件数据。
		-- 这里需要将请求地址替换为您实际的 Web 后台地址，并带上 myconf.py 中配置的 private_key。
		-- 使用 -q 参数进行静默下载，-O 指定输出文件为 SecondsTimerData.txt。
		execute("cd /home/tlbb/Server/SecondsTimer;wget -q 'http://127.0.0.1:8881/api/get_event?privateKey=YourPrivateKeyHere' -O SecondsTimerData.txt")
		
		-- 2. 打开刚刚下载的文本文件，准备读取数据
		local SecondsTimerData = openfile("./SecondsTimer/SecondsTimerData.txt", "r")
		if SecondsTimerData then
			-- 读取第一行数据 (API 返回的格式如: id,event,param1,param2,param3,param4)
			local DataStr = read(SecondsTimerData, "*l")
			closefile(SecondsTimerData)
			
			-- 3. 如果成功读取到了指令数据，则进行解析并执行
			if DataStr ~= nil then
				-- 使用 strfind 进行正则匹配，按照逗号分隔提取出 6 个字段
				local _,_,id,event,param1,param2,param3,param4 = strfind(DataStr,"(.*),(.*),(.*),(.*),(.*),(.*)")
				
				-- 根据事件名称 (event) 调用相应的处理函数
				if event == 'SendGlobalNews' then 
					-- 发送全服公告，param1 为公告内容
					x666898_SendGlobalNews(sceneId, param1)
				end
				
				if event == 'GivePlayerItem' then 
					-- 发放物品给指定玩家，param1: 角色名, param2: 物品ID, param3: 数量
					x666898_GivePlayerItem(sceneId, param1, param2, param3)
				end
				
				if event == 'SetPlayerLevel' then 
					-- 设置玩家等级，param1: 角色名, param2: 目标等级
					x666898_SetPlayerLevel(sceneId, param1, param2)
				end
				
				if event == 'GivePlayerYuanBao' then 
					-- 发放元宝，param1: 角色名, param2: 元宝数量
					x666898_GivePlayerYuanBao(sceneId, param1, param2)
				end
				
				-- 4. 执行完成后，将该事件的操作记录写入到本地日志文件中，方便运维审计
				local SecondsTimerLog = openfile("./SecondsTimer/SecondsTimerLog.txt", "a+")
				if SecondsTimerLog then
					write(SecondsTimerLog, "["..date('%Y-%m-%d %H:%M:%S').."][id]:"..id..",[Event]:"..event..",[Param1]:"..param1..",[Param2]:"..param2..",[Param3]:"..param3..",[Param4]:"..param4.."\n")
					closefile(SecondsTimerLog)
				end
			end
		end
	end
end

-- ==============================================================================
-- 函数名称: x666898_GetScenePlayerObjId
-- 功能描述: 遍历指定的一系列主城场景，根据玩家名称查找并返回其 ObjId
-- 参数列表:
--   PlayerName - 需要查找的玩家名称
-- 返回值  : 玩家的 ObjId，如果未找到则返回 0
-- 注意事项: 此为临时方案，当全服玩家较多时遍历场景效率较低
-- ==============================================================================
function x666898_GetScenePlayerObjId(PlayerName)
	-- 定义需要遍历搜索的主城场景 ID 列表
	local sceneIdList = {
		0,   -- 洛阳
		1,   -- 苏州
		2,   -- 大理
		186, -- 楼兰
	}
	local sId = nil
	local objId = 0

	-- 遍历所有指定的主城场景
	for _, tmpSceneId in pairs(sceneIdList) do
		-- 获取该场景内当前的人数
		local RenNum = LuaFnGetCopyScene_HumanCount(tmpSceneId)
		-- 遍历场景内的每一个玩家
		for i=0, RenNum-1 do
			local EveryBodyID = LuaFnGetCopyScene_HumanObjId(tmpSceneId, i)
			-- 对比玩家名称是否与要查找的名称匹配
			if GetName(tmpSceneId, EveryBodyID) == PlayerName then
				sId = tmpSceneId
				objId = EveryBodyID
				break
			end
		end
		-- 如果已经找到，则跳出外层循环
		if sId ~= nil then
			break
		end
	end

	return objId
end

-- ==============================================================================
-- 函数名称: x666898_SetPlayerLevel
-- 功能描述: 将当前场景内指定名称的玩家设置为目标等级，并播放特效和发送提示
-- ==============================================================================
function x666898_SetPlayerLevel(sceneId, PlayerName, level)
	local RenNum = LuaFnGetCopyScene_HumanCount( sceneId )
	for i=0, RenNum-1 do
		local EveryBodyID = LuaFnGetCopyScene_HumanObjId( sceneId, i )
		if GetName(sceneId, EveryBodyID) == PlayerName then
			-- 修改等级
			SetLevel(sceneId, EveryBodyID, level)
			-- 播放升级特效 (特效ID: 49)
			LuaFnSendSpecificImpactToUnit(sceneId, EveryBodyID, EveryBodyID, EveryBodyID, 49, 0)
			-- 给该玩家发送系统提示信息
			x666898_tips(sceneId, EveryBodyID, '管理员为您提升等级成功！')
		end
	end
end

-- ==============================================================================
-- 函数名称: x666898_GivePlayerItem
-- 功能描述: 将指定数量的物品发送到当前场景内指定玩家的背包中
-- ==============================================================================
function x666898_GivePlayerItem(sceneId, PlayerName, itemId, num)
	local RenNum = LuaFnGetCopyScene_HumanCount( sceneId )
	for i=0, RenNum-1 do
		local EveryBodyID = LuaFnGetCopyScene_HumanObjId( sceneId, i )
		if GetName(sceneId, EveryBodyID) == PlayerName then
			-- 开启添加物品的事务
			BeginAddItem(sceneId)
				-- 往事务中压入指定物品与数量
				AddItem(sceneId, itemId, num)
			EndAddItem(sceneId, EveryBodyID)
			-- 实际执行事务，将物品下发给玩家
			AddItemListToHuman(sceneId, EveryBodyID)
			-- 播放特效提示
			LuaFnSendSpecificImpactToUnit(sceneId, EveryBodyID, EveryBodyID, EveryBodyID, 49, 0)
			x666898_tips(sceneId, EveryBodyID, '管理员为您发放物品，请在背包中查收！')
		end
	end
end

-- ==============================================================================
-- 函数名称: x666898_GivePlayerYuanBao
-- 功能描述: 为当前场景内的指定玩家增加元宝
-- ==============================================================================
function x666898_GivePlayerYuanBao(sceneId, PlayerName, yuanbaoNum)
	local RenNum = LuaFnGetCopyScene_HumanCount( sceneId )
	for i=0, RenNum-1 do
		local EveryBodyID = LuaFnGetCopyScene_HumanObjId( sceneId, i )
		if GetName(sceneId, EveryBodyID) == PlayerName then
			-- 增加元宝，这里调用天龙服务端的 YuanBao 接口
			YuanBao(sceneId, EveryBodyID, -1, 1, yuanbaoNum)
			LuaFnSendSpecificImpactToUnit(sceneId, EveryBodyID, EveryBodyID, EveryBodyID, 49, 0)
			x666898_tips(sceneId, EveryBodyID, '管理员为您发放元宝：'..yuanbaoNum..' ，请注意查收！')
		end
	end
end

-- ==============================================================================
-- 函数名称: x666898_SendGlobalNews
-- 功能描述: 发送一条全局滚动屏幕公告，所有线上的玩家均可看到
-- ==============================================================================
function x666898_SendGlobalNews(sceneId, notice)
	-- 格式化公告字符串，使用系统标准格式发送
	local noticeFormat = format ("@*;SrvMsg;SCA:"..notice)
	AddGlobalCountNews(sceneId, noticeFormat)
end

-- ==============================================================================
-- 函数名称: x666898_tips
-- 功能描述: 向指定玩家发送屏幕中央的系统提示文本
-- ==============================================================================
function x666898_tips(sceneId, selfId, Tip)
	BeginEvent(sceneId)
		AddText(sceneId, Tip)
	EndEvent(sceneId)
	DispatchMissionTips(sceneId, selfId)
end