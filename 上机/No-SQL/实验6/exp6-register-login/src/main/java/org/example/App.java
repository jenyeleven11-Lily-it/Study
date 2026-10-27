package org.example;

import com.mongodb.MongoClientSettings;
import com.mongodb.ServerAddress;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import org.bson.Document;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * 实验六：综合案例注册登录
 * 使用 Java 结合 MongoDB 和 Redis，实现用户管理系统的注册、登录和获取用户列表功能
 */
public class App {
    // MongoDB 连接信息（虚拟机IP）
    private static final String MONGO_URI = "192.168.78.128";
    private static final int MONGO_PORT = 27017;
    private static final String DATABASE_NAME = "userdb";
    private static final String COLLECTION_NAME = "users";
    private static MongoCollection<Document> usersCollection;
    // Redis 连接信息（虚拟机IP）
    private static final String REDIS_HOST = "192.168.78.128";
    private static final int REDIS_PORT = 6379;
    private static JedisPool jedisPool;

    static {
        try {
            // 创建 MongoDB 连接池
            MongoClientSettings settings = MongoClientSettings.builder()
                    .applyToClusterSettings(builder ->
                            builder.hosts(Arrays.asList(new ServerAddress(MONGO_URI, MONGO_PORT))))
                    .build();
            usersCollection = MongoClients.create(settings).getDatabase(DATABASE_NAME).getCollection(COLLECTION_NAME);

            // 创建 Redis 连接池
            jedisPool = new JedisPool(REDIS_HOST, REDIS_PORT);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.println("1. Register");
            System.out.println("2. Login");
            System.out.println("3. Get Users");
            System.out.println("4. Exit");
            int choice = scanner.nextInt();
            scanner.nextLine();
            switch (choice) {
                case 1:
                    registerUser(scanner);
                    break;
                case 2:
                    loginUser(scanner);
                    break;
                case 3:
                    getUsers();
                    break;
                case 4:
                    jedisPool.close();
                    System.exit(0);
                default:
                    System.out.println("Invalid choice.");
            }
        }
    }

    private static void registerUser(Scanner scanner) {
        System.out.println("Enter username:");
        String username = scanner.nextLine();
        System.out.println("Enter password:");
        String password = scanner.nextLine();
        try {
            String hashedPassword = hashPassword(password);
            Document user = new Document("username", username).append("password", hashedPassword);
            usersCollection.insertOne(user);
            System.out.println("User registered successfully.");
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
    }

    private static void loginUser(Scanner scanner) {
        System.out.println("Enter username:");
        String username = scanner.nextLine();
        System.out.println("Enter password:");
        String password = scanner.nextLine();
        try {
            Document user = usersCollection.find(new Document("username", username)).first();
            if (user != null) {
                String hashedPassword = hashPassword(password);
                if (hashedPassword.equals(user.getString("password"))) {
                    // 从连接池获取 Redis 连接并设置用户登录状态
                    try (Jedis jedis = jedisPool.getResource()) {
                        jedis.set(username, "loggedIn");
                    }
                    System.out.println("Login successful.");
                } else {
                    System.out.println("Invalid username or password.");
                }
            } else {
                System.out.println("Invalid username or password.");
            }
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
    }

    private static void getUsers() {
        // 从连接池获取 Redis 连接
        try (Jedis jedis = jedisPool.getResource()) {
            String cachedUsers = jedis.get("users");
            if (cachedUsers != null) {
                System.out.println(cachedUsers);
            } else {
                List<Document> users = usersCollection.find().into(new ArrayList<>());
                String usersJson = users.toString();
                jedis.set("users", usersJson);
                System.out.println(usersJson);
            }
        }
    }

    private static String hashPassword(String password) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] hash = md.digest(password.getBytes());
        StringBuilder hexString = new StringBuilder();
        for (byte b : hash) {
            String hex = Integer.toHexString(0xff & b);
            if (hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        return hexString.toString();
    }
}
