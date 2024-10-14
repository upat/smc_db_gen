from pathlib import Path
import sys
import subprocess
import sqlite3
import time

# バッチファイルから引数ありで実行された場合の処理クラス
class CommonBaseClass:
	TYPE_FILE = True
	TYPE_FOLDER = False
	
	# 初期化(バッチファイルから入力されたパスの正否チェック)
	def __init__(self, input_type):
		self.init_result = True        # init処理結果
		self._input_path = sys.argv[1] # バッチ経由で入力されたパス
		
		# パスが絶対パスではない(空の文字列含む)場合
		if not Path(self._input_path).is_absolute():
			print('Not Absolute Path.')
			self.init_result = False
		# 入力パスが存在しない場合(バッチ経由なので基本通らない)
		elif not Path(self._input_path).exists():
			print('Not Found Input File.')
			self.init_result = False
		# ファイルの場合True、フォルダの場合Falseで判定
		elif Path(self._input_path).is_file() != input_type:
			print('This path is disable.')
			self.init_result = False
		else:
			pass
		
		# パスが不適切な場合、終了
		if not self.init_result:
			self.force_exit()
	
	# 強制終了時にコールする
	def force_exit(self):
		subprocess.run('pause', shell=True) # winbat pauseコマンド
		sys.exit()

# CommonBaseClassを継承したメイン処理クラス
class GenerateDB(CommonBaseClass):
	# 初期化
	def __init__(self, input_type):
		super().__init__(input_type) # 継承
		
		self._dbfile = Path(Path.cwd(), 'metadata.db') # dbファイルパス
		self._plfile = self._input_path                # playlistファイルパス
		self._plfilename = '"' + Path(self._input_path).stem + '"' # playlistファイル名
		self._unix_ms = str(int(time.time()) * 1000)   # UNIX時間(ミリ秒)
		
		# dbファイルが存在しない場合
		if not Path(self._dbfile).exists():
			print('Not Found db File.')
			super().force_exit()
		# 入力ファイルが.mpcplではない場合
		elif Path(self._input_path).suffix != '.mpcpl':
			print('This file is not mpcpl File.')
			super().force_exit()
		else:
			pass
	
	# dbファイル書き込み
	def gen_db(self):
		_smc_db = sqlite3.connect(self._dbfile)
		_smc_db_cur = _smc_db.cursor()

		# storagesテーブルのstorage_uuid取得
		_smc_db_cur.execute('SELECT storage_uuid FROM storages')
		_uuid_list = _smc_db_cur.fetchall()
		_uuid = '"' + _uuid_list[len(_uuid_list) - 1][0] + '"' # リスト最後尾の先頭データ
		
		# playlistsテーブルの_id取得→データ追加
		_smc_db_cur.execute('SELECT _id FROM playlists')
		_plid = self._getid_max(_smc_db_cur.fetchall()) + 1
		_plid_values = ','.join([ # VALUES部分の生成
			str(_plid),
			'1', self._plfilename,
			self._unix_ms,
			self._unix_ms,
			'NULL',
			'-1',
			'NULL'])
		_plid_command = self._create_sql('playlists', _plid_values)
		_smc_db_cur.execute(_plid_command)
		
		# playlist_membersテーブルの_id取得→データ追加
		_smc_db_cur.execute('SELECT _id FROM playlist_members')
		_plmembid = self._getid_max(_smc_db_cur.fetchall())
		for _index, _path in enumerate(self._mpcpl_read(), 1):
			_plmembid_values = ','.join([ # VALUES部分の生成
				str(_plmembid + _index),
				str(_plid), str(_index),
				_uuid,
				_path])
			_plmembid_command = self._create_sql('playlist_members', _plmembid_values)
			_smc_db_cur.execute(_plmembid_command)
			
		_smc_db.commit()
		_smc_db_cur.close()
		_smc_db.close()
	
	# プレイリスト読み出し
	def _mpcpl_read(self):
		try:
			# プレイリストファイル読み出し
			_open_data = open(self._plfile, 'r', encoding='utf-8')
			_read_data = _open_data.read().splitlines() # 末尾の改行無しで読み出し
		except:
			print('Text File not open.')
			super().force_exit()
		_dbpl_list = []
		# dbファイルのプレイリスト用のリスト作成
		for _text in _read_data:
			# [プレイリスト内の連番],filename,[楽曲ファイルのパス]で格納されているのでパス抽出
			if -1 < _text.find('filename,'):
				# mpcplファイル内の『filename,』以降の文字列を抽出してファイルパス取得
				_file_path = _text[_text.rfind('filename,'): ]
				# 3階層上のパスを取得(=アーティスト名フォルダの1階層上)
				_parent_path = str(Path(_file_path).parents[2])
				_file_path = _file_path.replace(_parent_path, '')
				_file_path = _file_path.replace("\\", "/") # バックスラッシュ→スラッシュ変換
				_dbpl_list.append('"Music' + _file_path + '"')
		return _dbpl_list
	
	# dbファイルから読み出したidデータの最大値を抽出
	def _getid_max(self, _idlist):
		_ret_idlist = []
		# (数値,)の形式で読み出されるため数値のみのリストに加工
		for _id in _idlist:
			_ret_idlist.append(int(_id[0]))
		return max(_ret_idlist) # 最大値return
	
	# sqlコマンド生成
	def _create_sql(self, _table, _values):
		_ret = ' '.join([ # コマンド生成
			'INSERT',
			'INTO',
			_table,
			'VALUES',
			'(' + _values + ')'])
		return _ret
