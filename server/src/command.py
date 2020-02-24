
from errorcode import ErrorCode
from msg import Msg


class Command:
    def __init__(self, event_console):
        self.login = False
        self.logout = False

        self.PushMsg = []

        self.login_id = None
        self.login_password = None
        self.logout = False
        self.close = False
        self.send_waterball_id = None
        self.send_waterball_content = None
        self.add_friend_id = None

        self.event = event_console

    def analyze(self, recv_msg: Msg):

        opt = recv_msg.get(Msg.key_opt)
        if opt == 'echo':
            res_msg = Msg(
                operate=opt,
                code=ErrorCode.Success,
                msg=recv_msg.get(Msg.key_msg)
            )
            self.push(res_msg)

        elif opt == 'login':
            ptt_id = recv_msg.get(Msg.key_payload)[Msg.key_ptt_id]
            ptt_pass = recv_msg.get(Msg.key_payload)[
                Msg.key_ptt_pass]

            for e in self.event.login:
                e(ptt_id, ptt_pass)

        elif opt == 'logout':
            for e in self.event.logout:
                e()

        elif opt == 'close':
            self.close = True

        elif opt == 'sendwaterball':
            self.send_waterball_id = recv_msg.get(Msg.key_payload)[Msg.key_ptt_id]
            self.send_waterball_content = recv_msg.get(Msg.key_payload)[Msg.key_content]

        elif opt == 'addfriend':
            self.add_friend_id = recv_msg.get(Msg.key_payload)[Msg.key_ptt_id]

        else:
            res_msg = Msg(
                operate=opt,
                code=ErrorCode.Unsupported,
                msg='Unsupported'
            )
            self.push(res_msg)

    def push(self, push_msg):
        self.PushMsg.append(push_msg.__str__())

    def sendWaterBall(self):
        temp_id, temp_content = self.send_waterball_id, self.send_waterball_content
        self.send_waterball_id, self.send_waterball_content = None, None
        return temp_id, temp_content

    def addfriend(self):
        temp = self.add_friend_id
        self.add_friend_id = None
        return temp
