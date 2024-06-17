Vue.component("modal", {
  template: "#modal-template"
});

// Edited, added more to input
var app = new Vue({
  el: "#app",
  data: {
      serviceURL: "https://cs3103.cs.unb.ca:8037",
      authenticated: false,
      loggedIn: null,
      input: {
          username: "",
          password: "",
          topicTitle: "",
          topicContent: "", 
          answerContent: "", 
          inputID: ""
      },
      topicResponse: "",
      answerResponse: "",
      answerResponseInTopics: "",
      searchTopicQuery: "", 
      searchAnswerQuery: "", 
      topicId: "", 
      answerTopicId: "", 
      topics: [], 
      answers: [] 
  },
  mounted: function() {
      axios
      .get(this.serviceURL+"/login")
      .then(response => {
          if (response.data.status == "success") {
              this.authenticated = true;
              this.loggedIn = response.data.user_id;
          }
      })
      .catch(error => {
          this.authenticated = false;
          console.log(error);
      });
  },
  methods: {
      login() {
          if (this.input.username != "" && this.input.password != "") {
              axios
              .post(this.serviceURL+"/login", {
                  "username": this.input.username,
                  "password": this.input.password
              })
              .then(response => {
                  if (response.data.status == "success") {
                      this.authenticated = true;
                      this.loggedIn = response.data.user_id;
                  }
              })
              .catch(e => {
                  alert("The username or password was incorrect, try again");
                  this.input.password = "";
                  console.log(e);
              });
          } else {
              alert("A username and password must be present");
          }
      },
      logout() {
          axios
          .delete(this.serviceURL+"/logout")
          .then(response => {
              location.reload();
          })
          .catch(e => {
              console.log(e);
          });
      },

      searchTopics(topicId){
        axios
        .get(`${this.serviceURL}/topics/${this.searchTopicQuery}`)
        .then(response => {
            const topicData = response.data;
            const topic = topicData["Topic"];
            delete topicData["Topic"];
            let formattedJson = `Topic: ${JSON.stringify(topic[1])}`;
            formattedJson += `\n ${JSON.stringify(topic[2])}`;
            this.topicResponse = formattedJson;
        })
        .catch(e => {
          alert("ERROR");
          console.log(e);
        });
    },

    searchAnswersByTopicId(topicId){
        axios
          .get(`${this.serviceURL}/answers/${this.searchAnswerQuery}`)
          .then(response => {
            const answerData = response.data;
            const answers = answerData["Answers"];
            let formattedJson = "Answers:\n";
            answers.forEach(answer => {
              formattedJson += `  ID: ${answer[0]}\n`;
              formattedJson += `  Content: ${answer[1]}\n`;
              formattedJson += `  User: ${answer[2]}\n`;
            });
            this.answerResponse = formattedJson;
          })
          .catch(e => {
            alert("ERROR");
            console.log(e);
          });
      },

      searchAnswersByTopicIdInTopic(topicId){
        axios
          .get(`${this.serviceURL}/answers/${this.searchTopicQuery}`)
          .then(response => {
            const answerData = response.data;
            const answers = answerData["Answers"];
            let formattedJson = "Answers:\n";
            answers.forEach(answer => {
              formattedJson += `  ID: ${answer[0]}\n`;
              formattedJson += `  Content: ${answer[1]}\n`;
              formattedJson += `  User: ${answer[2]}\n`;
              formattedJson += `\n`;
            });
            this.answerResponseInTopics = formattedJson;
          })
          .catch(e => {
            alert("ERROR");
            console.log(e);
          });
      },

      deleteTopic(topicId) {
        if (confirm("Are you sure you want to delete this topic?")) {
          axios
            .delete(`${this.serviceURL}/topics/${topicId}`)
            .then(response => {
              alert("Topic deleted successfully!");
            })
            .catch(e => {
              alert("Error deleting topic");
              console.log(e);
            });
        }
      },

      deleteAnswer(answerId) {
        if (confirm("Are you sure you want to delete this topic?")) {
          axios
            .delete(`${this.serviceURL}/answers/${answerId}`)
            .then(response => {
              alert("Answer deleted successfully!");
            })
            .catch(e => {
              alert("Error deleting answer");
              console.log(e);
            });
        }
      },

      postTopic() {
        axios
          .post(this.serviceURL + "/topic"
          , {
            "topic_title": this.input.topicTitle,
            "content": this.input.topicContent
          })
          .then(response => {
            alert("Topic posted successfully!");
            this.input.topicTitle = "";
            this.input.topicContent = "";
          })
          .catch(e => {
            alert("Error posting topic");
            console.log(e);
          });
      },
 
      postAnswer() {
          axios
          .post(`${this.serviceURL}/answer`, {
              "answer_content": this.input.answerContent,
              "topic_id": this.input.inputID
          })
          .then(response => {
              alert("Answer posted successfully!");
              this.input.inputID = "";
              this.input.answerContent = "";
          })
          .catch(e => {
              alert("Error posting answer");
              console.log(e);
          });
      }
  }
});
