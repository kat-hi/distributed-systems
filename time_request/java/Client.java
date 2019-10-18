import java.net.InetAddress;
import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Locale;
import java.io.*;

public class Client {

    public static void getServerInfos(Socket socket, String peername, int port) {
        try {
            InetAddress address = InetAddress.getByName(peername);
            System.out.println("Connection established: " +  address + ":" + port);
        } catch ( IOException e ) {
            e.printStackTrace();
        }
    }

    public static void sendHeader(Socket socket, String[] header) throws IOException {
        PrintWriter pw = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
        for(String line : header) {
            pw.print(line);
            pw.flush();
        }
    }

    public static void receive(Socket socket) throws IOException {
        ArrayList<String> headerLines = new ArrayList<String>();
        BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        for (int i = 0; i<4;i++) {
            headerLines.add(br.readLine());
        }
        String dateRaw = headerLines.get(3);
        SimpleDateFormat simpleDate = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssX", Locale.ENGLISH);
        try {
            Date dateParse = simpleDate.parse(dateRaw);
            System.out.println("Current time on the server: " + dateParse);
        } catch ( Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String args[]) {
        String[] header = {"dslp/2.0\r\n", "request time\r\n", "dslp/body\r\n"};
        String[] messageType = {"request time", "response time", "group join", "group leave", "group notify",
                "user join", "user leave", "user text notify", "user file notify", "error"};
        String peername = "dbl44.beuth-hochschule.de";
        int port = 21;
        Socket socket;

        try {
            socket = new Socket(peername, port);
            getServerInfos(socket, peername, port);
            sendHeader(socket, header);
            receive(socket);
        } catch (IOException e ) {
            e.printStackTrace();
        }
    }
}
