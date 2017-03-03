package edu.hofstra.socialup.socialup;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONTokener;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Scanner;

public class EventActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    public String username = "giewev";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_event);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        String currentTopic = getIntent().getExtras().getString("topic");

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        //blackmagic
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();

        StrictMode.setThreadPolicy(policy);

        //gets list of all users
        URL url = null;
        String jsonUsers = "";
        JSONArray values = new JSONArray();
        try {
            url = new URL("http://54.146.138.252:5000/events");
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }


        try {
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();

            try {

                InputStream in = new BufferedInputStream(urlConnection.getInputStream());
                Scanner scanner = new Scanner(in).useDelimiter(".");
                jsonUsers = scanner.next();
            } finally {
                urlConnection.disconnect();
            }
        } catch (IOException e) {

        }
        try {
            values = (JSONArray) new JSONTokener(jsonUsers).nextValue();

        } catch (JSONException e){

        }

        final ListView listview = (ListView) findViewById(R.id.event_list);


        final ArrayList<String> list = new ArrayList<String>();
        try{
            for (int i = 0; i < values.length(); i++) {
                JSONObject event = (JSONObject) values.get(i);

                String topicName = event.getString("topic_name");
                if("Switch".compareTo(topicName) == 0)
                    list.add(event.getString("name"));
            }
        } catch (JSONException e){

        }


        ArrayAdapter adapter = new ArrayAdapter(this, android.R.layout.simple_list_item_1, list);
        listview.setAdapter(adapter);
        final Context context = this;
        listview.setOnItemClickListener(new AdapterView.OnItemClickListener() {

            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {

                //Toast.makeText(context, "WORKS", Toast.LENGTH_SHORT).show();
            }

        });
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.event, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_profile) {
            Intent k = new Intent(EventActivity.this, ProfileActivity.class);
            startActivity(k);
        } else if (id == R.id.nav_friends) {
            Intent k = new Intent(EventActivity.this, FriendsActivity.class);
            startActivity(k);
        } else if (id == R.id.nav_mytopics) {
            Intent k = new Intent(EventActivity.this, MyTopicsActivity.class);
            startActivity(k);
        } else if (id == R.id.nav_searchtopics) {
            Intent k = new Intent(EventActivity.this, SearchTopicsActivity.class);
            startActivity(k);
        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }
}
