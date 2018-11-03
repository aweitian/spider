package zsh.jl.spider;

import android.os.Process;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.inputmethodservice.InputMethodService;
import android.os.IBinder;
import android.util.Base64;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.inputmethod.InputConnection;
import android.widget.Toast;

public class AdbIME extends InputMethodService {
//    public static AdbIME instance;
    private String IME_MESSAGE = "ADB_INPUT_TEXT";
    private String IME_CHARS = "ADB_INPUT_CHARS";
    private String IME_KEYCODE = "ADB_INPUT_CODE";
    private String IME_EDITORCODE = "ADB_EDITOR_CODE";
    private String IME_MESSAGE_B64 = "ADB_INPUT_B64";
    private BroadcastReceiver mReceiver = null;
//
//    public AdbIME() {
//        AdbIME.instance = this;
//}

    @Override
    public View onCreateInputView() {
        View mInputView = getLayoutInflater().inflate(R.layout.view, null);
        Log.d("Garri","AdbIME::onCreateInputView");
        int pid = Process.myPid();
        Log.d("Garri","AdbIME::my pid is:" + pid);
//        AdbIME.instance = this;
//        System.out.print("onCreateInputView");
        if (mReceiver == null) {
            IntentFilter filter = new IntentFilter(IME_MESSAGE);
            filter.addAction(IME_CHARS);
            filter.addAction(IME_KEYCODE);
            filter.addAction(IME_EDITORCODE);
            filter.addAction(IME_MESSAGE_B64);
            mReceiver = new AdbReceiver();
            registerReceiver(mReceiver, filter);
        }
        Toast.makeText(getApplicationContext(), "AdbIME", Toast.LENGTH_SHORT).show();
        return mInputView;
    }

    public void onDestroy() {
//        if (mReceiver != null)
//            unregisterReceiver(mReceiver);
        super.onDestroy();
    }

//    public void setText(String text) {
//        InputConnection ic = getCurrentInputConnection();
//        if (ic != null) {
//            if (ic.commitText(text, 1)) {
//                System.out.print("IC commit ok");
//            } else {
//                System.out.print("IC commit fail");
//            }
//        } else {
//            System.out.print("IC is null");
//        }
//    }

    class AdbReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (intent.getAction().equals(IME_MESSAGE)) {
                String msg = intent.getStringExtra("msg");
                if (msg != null) {
                    InputConnection ic = getCurrentInputConnection();
                    if (ic != null)
                        ic.commitText(msg, 1);
                }
            }

            if (intent.getAction().equals(IME_MESSAGE_B64)) {
                String data = intent.getStringExtra("msg");

                byte[] b64 = Base64.decode(data, Base64.DEFAULT);
                String msg = "NOT SUPPORTED";
                try {
                    msg = new String(b64, "UTF-8");
                } catch (Exception e) {

                }

                if (msg != null) {
                    InputConnection ic = getCurrentInputConnection();
                    if (ic != null)
                        ic.commitText(msg, 1);
                }
            }

            if (intent.getAction().equals(IME_CHARS)) {
                int[] chars = intent.getIntArrayExtra("chars");
                if (chars != null) {
                    String msg = new String(chars, 0, chars.length);
                    InputConnection ic = getCurrentInputConnection();
                    if (ic != null)
                        ic.commitText(msg, 1);
                }
            }

            if (intent.getAction().equals(IME_KEYCODE)) {
                int code = intent.getIntExtra("code", -1);
                if (code != -1) {
                    InputConnection ic = getCurrentInputConnection();
                    if (ic != null)
                        ic.sendKeyEvent(new KeyEvent(KeyEvent.ACTION_DOWN, code));
                }
            }

            if (intent.getAction().equals(IME_EDITORCODE)) {
                int code = intent.getIntExtra("code", -1);
                if (code != -1) {
                    InputConnection ic = getCurrentInputConnection();
                    if (ic != null)
                        ic.performEditorAction(code);
                }
            }
        }
    }
}
